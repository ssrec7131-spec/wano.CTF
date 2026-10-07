import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';

// ─── Floating Ember Particles ───────────────────────────────────────────────
const EMBERS = Array.from({ length: 28 }, (_, i) => ({
  id: i,
  x: Math.random() * 100,
  size: Math.random() * 3 + 1.5,
  delay: Math.random() * 8,
  duration: Math.random() * 8 + 10,
  drift: (Math.random() - 0.5) * 120,
  color: i % 3 === 0 ? '#E5A93C' : i % 3 === 1 ? '#E02F3E' : '#3CDCF0',
}));

export const FloatingEmbers: React.FC = () => (
  <div className="pointer-events-none absolute inset-0 overflow-hidden">
    {EMBERS.map((e) => (
      <motion.span
        key={e.id}
        className="absolute bottom-0 rounded-full"
        style={{
          left: `${e.x}%`,
          width: e.size,
          height: e.size,
          background: e.color,
          boxShadow: `0 0 ${e.size * 3}px ${e.color}`,
        }}
        animate={{
          y: [0, -window.innerHeight - 100],
          x: [0, e.drift],
          opacity: [0, 0.9, 0.6, 0],
          scale: [1, 1.5, 0.5, 0],
        }}
        transition={{
          duration: e.duration,
          delay: e.delay,
          repeat: Infinity,
          ease: 'easeOut',
        }}
      />
    ))}
  </div>
);

// ─── Animated Grid Lines ─────────────────────────────────────────────────────
export const AnimatedGrid: React.FC<{ className?: string }> = ({ className }) => (
  <motion.div
    className={`pointer-events-none absolute inset-0 ${className ?? ''}`}
    style={{
      backgroundImage:
        'linear-gradient(rgba(229,169,60,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(229,169,60,0.06) 1px, transparent 1px)',
      backgroundSize: '46px 46px',
    }}
    animate={{ backgroundPosition: ['0px 0px', '46px 46px'] }}
    transition={{ duration: 12, repeat: Infinity, ease: 'linear' }}
  />
);

// ─── Binary Rain Column ───────────────────────────────────────────────────────
const CHARS = '01アイウエオカキクケコサシスセソ∑Σ∏∆';
function randomChars(n: number) {
  return Array.from({ length: n }, () => CHARS[Math.floor(Math.random() * CHARS.length)]).join('\n');
}

const COLS = Array.from({ length: 18 }, (_, i) => ({
  id: i,
  x: (i / 18) * 100 + Math.random() * 5,
  chars: randomChars(32),
  delay: Math.random() * 6,
  duration: Math.random() * 6 + 10,
  opacity: Math.random() * 0.18 + 0.04,
}));

export const BinaryRain: React.FC = () => (
  <div className="pointer-events-none absolute inset-0 overflow-hidden select-none">
    {COLS.map((col) => (
      <motion.pre
        key={col.id}
        className="absolute top-0 font-mono text-[10px] leading-[1.45] whitespace-pre"
        style={{
          left: `${col.x}%`,
          color: '#3CDCF0',
          opacity: col.opacity,
          letterSpacing: '0.2em',
        }}
        animate={{ y: ['-100%', '120%'] }}
        transition={{
          duration: col.duration,
          delay: col.delay,
          repeat: Infinity,
          ease: 'linear',
        }}
      >
        {col.chars}
      </motion.pre>
    ))}
  </div>
);

// ─── Blood Moon Pulse ─────────────────────────────────────────────────────────
export const BloodMoonGlow: React.FC = () => (
  <motion.div
    className="pointer-events-none absolute top-[-10%] left-1/2 -translate-x-1/2"
    style={{ width: 600, height: 600 }}
    animate={{
      scale: [1, 1.12, 1],
      opacity: [0.35, 0.55, 0.35],
    }}
    transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
  >
    <div
      className="w-full h-full rounded-full"
      style={{
        background: 'radial-gradient(circle at 50% 50%, rgba(224,47,62,0.45) 0%, rgba(229,169,60,0.12) 40%, transparent 75%)',
        filter: 'blur(60px)',
      }}
    />
  </motion.div>
);

// ─── Scan Beam ───────────────────────────────────────────────────────────────
export const ScanBeam: React.FC = () => (
  <motion.div
    className="pointer-events-none absolute left-0 right-0"
    style={{
      height: '2px',
      background: 'linear-gradient(90deg, transparent, rgba(60,220,240,0.6), rgba(229,169,60,0.4), transparent)',
    }}
    animate={{ top: ['0%', '100%'], opacity: [0, 1, 1, 0] }}
    transition={{ duration: 4, repeat: Infinity, ease: 'linear', repeatDelay: 2 }}
  />
);

// ─── Canvas Particle System (WebGL-style dot stars) ───────────────────────────
export const StarField: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.2 + 0.3,
      a: Math.random(),
      da: (Math.random() - 0.5) * 0.008,
    }));

    let raf: number;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((s) => {
        s.a += s.da;
        if (s.a <= 0 || s.a >= 1) s.da = -s.da;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(203,216,228,${s.a * 0.6})`;
        ctx.fill();
      });
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => cancelAnimationFrame(raf);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none absolute inset-0 w-full h-full"
    />
  );
};

// ─── Cinematic Video Background ──────────────────────────────────────────────
export interface VideoBackgroundProps {
  src?: string;
  videos?: { id: number; label: string; src: string; desc: string }[];
  className?: string;
  opacity?: number;
  showScanlines?: boolean;
  showVignette?: boolean;
  showGrid?: boolean;
  showHudControls?: boolean;
  autoCycle?: boolean;
}

const DEFAULT_VIDEOS = [
  { id: 1, label: '01', src: '/vid1.mp4', desc: 'Warzone Sector Alpha' },
  { id: 2, label: '02', src: '/vid2.mp4', desc: 'Poneglyph Vault Grid' },
  { id: 3, label: '03', src: '/vid3.mp4', desc: 'Marine Recon Stream' },
];

export const VideoBackground: React.FC<VideoBackgroundProps> = ({
  src,
  videos = DEFAULT_VIDEOS,
  className = '',
  opacity = 1.0,
  showScanlines = false,
  showVignette = true,
  showGrid = false,
  showHudControls = true,
  autoCycle = true,
}) => {
  const [activeIdx, setActiveIdx] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isMuted, setIsMuted] = useState(true);
  const [isFading, setIsFading] = useState(false);
  const [clarityLevel, setClarityLevel] = useState<number>(opacity);
  const videoRef = useRef<HTMLVideoElement>(null);

  const currentVideo = videos[activeIdx] || videos[0];
  const videoSrc = src || currentVideo?.src || '/vid1.mp4';

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    video.load();
    video.play().catch(() => setIsPlaying(false));
  }, [videoSrc]);

  const changeVideo = (newIdx: number) => {
    if (newIdx === activeIdx) return;
    setIsFading(true);
    setTimeout(() => {
      setActiveIdx(newIdx);
      setIsFading(false);
    }, 180);
  };

  const handleNext = () => {
    const nextIdx = (activeIdx + 1) % videos.length;
    changeVideo(nextIdx);
  };

  const handleEnded = () => {
    if (autoCycle && videos.length > 1) {
      handleNext();
    }
  };

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    const nextMuted = !videoRef.current.muted;
    videoRef.current.muted = nextMuted;
    setIsMuted(nextMuted);
  };

  const toggleClarity = () => {
    if (clarityLevel >= 0.95) setClarityLevel(0.7);
    else if (clarityLevel >= 0.65) setClarityLevel(0.45);
    else setClarityLevel(1.0);
  };

  return (
    <div className={`pointer-events-none absolute inset-0 overflow-hidden ${className}`}>
      {/* HTML5 Background Video - Crystal Clear Presentation */}
      <video
        ref={videoRef}
        key={videoSrc}
        src={videoSrc}
        autoPlay
        loop={!autoCycle || videos.length <= 1}
        muted
        playsInline
        preload="auto"
        onEnded={handleEnded}
        className={`absolute inset-0 h-full w-full object-cover object-center transition-opacity duration-300 ${
          isFading ? 'opacity-0' : ''
        }`}
        style={{
          opacity: isFading ? 0 : clarityLevel,
          filter: 'contrast(1.04) brightness(1.02)',
        }}
      />

      {/* Cyberpunk Scanlines (optional & subtle) */}
      {showScanlines && (
        <div
          className="pointer-events-none absolute inset-0 opacity-10 mix-blend-overlay"
          style={{
            backgroundImage:
              'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 0, 0, 0.6) 2px, rgba(0, 0, 0, 0.6) 4px)',
          }}
        />
      )}

      {/* Tech Grid (optional) */}
      {showGrid && (
        <div
          className="pointer-events-none absolute inset-0 opacity-10"
          style={{
            backgroundImage:
              'linear-gradient(rgba(60,220,240,0.15) 1px, transparent 1px), linear-gradient(90deg, rgba(60,220,240,0.15) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
      )}

      {/* Subtle Perimeter Edge Vignette - Keeps center 80% completely clear */}
      {showVignette && (
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse at center, transparent 72%, rgba(5,7,10,0.4) 95%, rgba(5,7,10,0.7) 100%)',
          }}
        />
      )}

      {/* Soft bottom edge blend into the next section */}
      <div className="pointer-events-none absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-background via-background/40 to-transparent" />

      {/* Floating HUD controls for video switching, audio & playback */}
      {showHudControls && (
        <div className="pointer-events-auto absolute bottom-5 right-5 z-30 flex items-center gap-2 rounded-full border border-gold/40 bg-void/90 px-3.5 py-1.5 font-mono text-[11px] text-steel-200 shadow-[0_4px_20px_rgba(0,0,0,0.8)] backdrop-blur-md transition-all hover:border-gold">
          {/* Feed Switcher Tabs (VID 01 / 02 / 03) */}
          <div className="flex items-center gap-1 border-r border-steel-700/70 pr-2">
            <span className="text-[10px] text-gold font-bold uppercase tracking-wider hidden sm:inline mr-1">
              FEED:
            </span>
            {videos.map((item, idx) => (
              <button
                key={item.id}
                type="button"
                onClick={() => changeVideo(idx)}
                className={`px-2 py-0.5 rounded transition-all font-bold text-[11px] ${
                  activeIdx === idx
                    ? 'bg-gold/30 text-gold border border-gold/70 shadow-[0_0_10px_rgba(229,169,60,0.6)]'
                    : 'text-steel-400 hover:text-white hover:bg-steel-800/60'
                }`}
                title={`Switch to ${item.desc} (${item.src})`}
              >
                {item.label}
              </button>
            ))}
          </div>

          {/* Clarity toggle */}
          <button
            type="button"
            onClick={toggleClarity}
            className="flex items-center gap-1 px-1.5 py-0.5 rounded hover:bg-steel-800/60 transition-colors text-steel-300 hover:text-gold"
            title="Toggle Video Brightness / Clarity"
          >
            <span className="text-[10px] text-gold/90 font-bold">
              {clarityLevel >= 0.95 ? '🔆 100%' : clarityLevel >= 0.65 ? '🌤️ 70%' : '🌙 45%'}
            </span>
          </button>

          <span className="text-steel-700">|</span>

          {/* Play/Pause Toggle */}
          <button
            type="button"
            onClick={togglePlay}
            className="flex items-center gap-1.5 transition-colors hover:text-gold focus:outline-none"
            title={isPlaying ? 'Pause Background Video' : 'Resume Background Video'}
          >
            {isPlaying ? (
              <span className="flex items-center gap-1 text-cyber-green font-semibold">
                <span className="h-1.5 w-1.5 rounded-full bg-cyber-green animate-ping" />
                <span>LIVE</span>
              </span>
            ) : (
              <span className="text-steel-500">PAUSED</span>
            )}
          </button>

          <span className="text-steel-700">|</span>

          {/* Audio Mute/Unmute Toggle */}
          <button
            type="button"
            onClick={toggleMute}
            className="flex items-center gap-1 transition-colors hover:text-gold focus:outline-none"
            title={isMuted ? 'Unmute Audio' : 'Mute Audio'}
          >
            {isMuted ? '🔇 MUTE' : '🔊 AUDIO'}
          </button>
        </div>
      )}
    </div>
  );
};

