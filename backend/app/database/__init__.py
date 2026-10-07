"""Database package — re-exports the canonical engine/session singletons.

Import from ``app.database`` throughout the codebase; the concrete
implementation (Turso / aiosqlite) is selected at startup from env vars.
"""

from app.database.turso_connection import (
    SessionLocal,
    check_database,
    dispose_engine,
    engine,
    get_session,
    session_scope,
)

__all__ = [
    "engine",
    "SessionLocal",
    "get_session",
    "session_scope",
    "dispose_engine",
    "check_database",
]
