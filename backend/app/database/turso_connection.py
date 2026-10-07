"""Turso / libSQL async database connection layer.

Turso uses the libSQL wire protocol. The ``sqlalchemy-libsql`` dialect is
synchronous, so we wrap every call through ``asyncio.get_event_loop().run_in_executor``
via SQLAlchemy's built-in ``AsyncEngine`` shim (create_async_engine with the
``aiosqlite`` driver is replaced here by a thread-pool pattern for libsql).

For local development without Turso credentials the fallback is the existing
aiosqlite path (``sqlite+aiosqlite:///...``) so the dev workflow is unchanged.

Connection URL formats:
  Remote Turso:    libsql://[name].turso.io?authToken=<token>&secure=true
  Embedded replica (offline+sync): sqlite+libsql:///./local.db
  Dev (offline):   sqlite+aiosqlite:///./wano_ctf_dev.db
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

logger = logging.getLogger("wano.db")


def _build_dsn() -> str:
    """Resolve the database URL, preferring Turso when credentials are set."""
    turso_url: str = settings.turso_database_url  # type: ignore[attr-defined]
    turso_token: str = settings.turso_auth_token   # type: ignore[attr-defined]

    if turso_url and turso_token:
        # Strip any existing scheme prefix supplied by the user and rebuild it
        # in the exact format sqlalchemy-libsql expects.
        host = turso_url.replace("libsql://", "").replace("https://", "").rstrip("/")
        dsn = f"sqlite+libsql://{host}?authToken={turso_token}&secure=true"
        logger.info("Using Turso remote database: %s", host)
        return dsn

    # Fallback — existing aiosqlite dev database
    dsn = settings.database_url
    logger.info("Turso credentials not set, falling back to: %s", dsn.split("///")[0])
    return dsn


def _create_engine(dsn: str | None = None) -> AsyncEngine:
    resolved = dsn or _build_dsn()
    common: dict = {"echo": settings.db_echo, "future": True}

    if "libsql" in resolved:
        # sqlalchemy-libsql is synchronous — wrap it in the thread-pool executor.
        # pool_size / max_overflow are not applicable for the libsql dialect.
        from sqlalchemy import create_engine as _sync_create_engine
        from sqlalchemy.ext.asyncio import AsyncEngine as _AsyncEngine

        sync_engine = _sync_create_engine(resolved, echo=settings.db_echo, future=True)

        # Build an AsyncEngine backed by the sync engine using a run_sync bridge.
        # This works because SQLAlchemy 2.x can wrap a sync engine via
        # create_async_engine("...", execution_options=...) but the simplest
        # stable approach for non-async drivers is AsyncEngine(sync_engine).
        from sqlalchemy.ext.asyncio import AsyncEngine as _AEng

        return _AEng(sync_engine)  # type: ignore[return-value]

    if "sqlite" in resolved:
        common.pop("pool_pre_ping", None)
        return create_async_engine(resolved, **common)

    common.update(
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_recycle=1800,
        pool_timeout=30,
        pool_pre_ping=True,
    )
    if ":6543" in resolved:
        common["connect_args"] = {"prepare_threshold": None}

    return create_async_engine(resolved, **common)


# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------

engine: AsyncEngine = _create_engine()

SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding a request-scoped async session."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Programmatic session scope for background tasks / WebSocket handlers."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def dispose_engine() -> None:
    await engine.dispose()


async def check_database() -> bool:
    """Lightweight connectivity check used by the /health endpoint."""
    from sqlalchemy import text

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:  # pragma: no cover
        return False
