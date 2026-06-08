import logging
import logging.handlers
import os
import sys
from datetime import datetime
import warnings

import numpy as np
from pydub import AudioSegment

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import torch
    import torch.serialization
    from bark import SAMPLE_RATE, generate_audio, preload_models
except ImportError as exc:
    raise ImportError(
        "Bark is required. Install with: pip install -r requirements.txt"
    ) from exc

# Ensure console output uses UTF-8 on Windows if possible
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Setup comprehensive logging to both file and console
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"ai_song_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.info("=" * 70)
logger.info("AI Song Generator Initialized")
logger.info("Log file: %s", LOG_FILE)
logger.info("=" * 70)

# Fix PyTorch 2.6 weights_only issue
try:
    torch.serialization.add_safe_globals([np.core.multiarray.scalar])
    logger.info("PyTorch safe_globals configured")
except Exception as e:
    logger.warning("PyTorch safe_globals configuration warning: %s", e)

STYLE_PROMPTS = {
    "إلكتروني": "A bright and modern electronic pop backing track with synth pads, soft beats, and a futuristic atmosphere.",
    "حماسي": "An energetic and stadium-style backing track with driving percussion, bold chords, and uplifting cinematic energy.",
    "هادئ": "A calm ambient background with soft pads, gentle piano, and a relaxing modern atmosphere.",
    "درامي": "A dramatic and cinematic score with tense strings, wide orchestral textures, and powerful rhythmic motion.",
}

VOICE_PROMPTS = {
    "إلكتروني": "Sing the following lyrics in an electronic pop style with a clear and bright tone.",
    "حماسي": "Sing the following lyrics in an energetic stadium singing style with passion and power.",
    "هادئ": "Sing the following lyrics in a gentle and emotional tone with soft phrasing.",
    "درامي": "Sing the following lyrics in a dramatic performance style with intensity and depth.",
}

MODEL_LOADED = False
DEFAULT_STYLE = "إلكتروني"
MIN_TEMPO = 40
MAX_TEMPO = 240


def initialize_models():
    """Preload Bark models once to reduce repeated startup cost.
    
    Handles PyTorch 2.6+ weights_only issue by patching torch.load.
    """
    global MODEL_LOADED
    if MODEL_LOADED:
        logger.info("Models already loaded, skipping initialization")
        return
    
    try:
        logger.info("Starting Bark model preload (this may take a few minutes on first run)...")
        
        # Monkey-patch torch.load to use weights_only=False for Bark models
        original_torch_load = torch.load
        
        def patched_torch_load(*args, **kwargs):
            """Wrapper that disables weights_only for trusted Bark checkpoints."""
            logger.debug("torch.load called with args=%s kwargs=%s", args, kwargs)
            if 'weights_only' not in kwargs:
                kwargs['weights_only'] = False
                logger.debug("Set weights_only=False for torch.load")
            try:
                return original_torch_load(*args, **kwargs)
            except Exception as e:
                logger.error("Failed torch.load with weights_only=%s: %s", kwargs.get('weights_only'), e)
                raise
        
        torch.load = patched_torch_load
        logger.info("PyTorch load patched successfully")
        
        preload_models()
        MODEL_LOADED = True
        logger.info("All Bark models loaded successfully")
        
    except Exception as exc:
        logger.error("Failed to preload Bark models: %s", exc, exc_info=True)
        raise


def validate_style(style: str) -> str:
    """Ensure the selected style is valid."""
    if style not in STYLE_PROMPTS:
        logger.warning("Invalid style '%s'; falling back to '%s'.", style, DEFAULT_STYLE)
        return DEFAULT_STYLE
    logger.debug("Style validated: %s", style)
    return style


def validate_tempo(tempo_override):
    """Validate tempo input and clamp it to a safe range."""
    if tempo_override is None:
        logger.debug("No tempo override provided, using style default")
        return None
    try:
        tempo = int(tempo_override)
    except (TypeError, ValueError):
        logger.warning("Invalid tempo '%s'; using default tempo.", tempo_override)
        return None
    clamped_tempo = max(MIN_TEMPO, min(MAX_TEMPO, tempo))
    logger.debug("Tempo validated: input=%s, clamped=%d", tempo_override, clamped_tempo)
    return clamped_tempo


def ensure_audio_array(audio_array) -> np.ndarray:
    """Convert Bark output to a mono numpy float32 array."""
    audio_array = np.asarray(audio_array)
    if audio_array.ndim > 1:
        audio_array = np.squeeze(audio_array)
    if audio_array.dtype != np.float32:
        audio_array = audio_array.astype(np.float32)
    return audio_array


def audio_segment_from_array(audio_array) -> AudioSegment:
    """Convert a numpy audio array into a pydub AudioSegment."""
    audio_array = ensure_audio_array(audio_array)
    audio_int16 = np.clip(audio_array * 32767, -32768, 32767).astype(np.int16)
    return AudioSegment(
        audio_int16.tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=2,
        channels=1,
    )


def safe_generate_audio(prompt: str, history_prompt=None, text_temp: float = 0.7, waveform_temp: float = 0.7):
    """Generate audio using Bark and retry without history_prompt if needed."""
    try:
        return generate_audio(
            prompt,
            history_prompt=history_prompt,
            text_temp=text_temp,
            waveform_temp=waveform_temp,
        )
    except ValueError as exc:
        if "history prompt not found" in str(exc).lower():
            logger.warning("History prompt not found: %s. Retrying without history_prompt.", history_prompt)
            return generate_audio(
                prompt,
                text_temp=text_temp,
                waveform_temp=waveform_temp,
            )
        raise


def create_vocal_track(lyrics_text: str, style: str, tempo: int | None) -> AudioSegment:
    """Generate a vocal track for the lyrics and selected style."""
    logger.info("Generating vocal track: style=%s, lyrics_length=%d, tempo=%s", 
                style, len(lyrics_text), tempo or 120)
    prompt = (
        f"{VOICE_PROMPTS[style]}\n"
        f"Tempo: {tempo if tempo else 120} BPM\n"
        f"Lyrics:\n{lyrics_text}"
    )
    try:
        logger.debug("Calling generate_audio for vocal with prompt length: %d", len(prompt))
        audio_array = safe_generate_audio(
            prompt,
            history_prompt="v2/singing",
            text_temp=0.7,
            waveform_temp=0.7,
        )
        logger.info("Vocal track generated successfully (length: %.2f seconds)", 
                    len(audio_array) / SAMPLE_RATE)
    except Exception as exc:
        logger.error("Vocal generation failed: %s", exc, exc_info=True)
        raise
    return audio_segment_from_array(audio_array)


def create_background_track(style: str, duration_ms: int, tempo: int | None) -> AudioSegment:
    """Generate a background music track for the style."""
    logger.info("Generating background track: style=%s, target_duration=%dms, tempo=%s", 
                style, duration_ms, tempo or 120)
    prompt = (
        f"{STYLE_PROMPTS[style]}\n"
        f"Tempo: {tempo if tempo else 120} BPM"
    )
    try:
        logger.debug("Calling generate_audio for background with prompt length: %d", len(prompt))
        audio_array = generate_audio(
            prompt,
            text_temp=0.75,
            waveform_temp=0.7,
        )
        logger.info("Background track generated successfully (length: %.2f seconds)", 
                    len(audio_array) / SAMPLE_RATE)
    except Exception as exc:
        logger.error("Background generation failed: %s", exc, exc_info=True)
        raise
    background_segment = audio_segment_from_array(audio_array)
    if len(background_segment) < duration_ms:
        silence_duration = duration_ms - len(background_segment)
        logger.debug("Adding %dms of silence to background", silence_duration)
        background_segment = background_segment + AudioSegment.silent(duration=silence_duration)
    return background_segment[:duration_ms]


def mix_tracks(vocal: AudioSegment, background: AudioSegment) -> AudioSegment:
    """Overlay vocal and background tracks and normalize the result."""
    logger.info("Mixing vocal (%.2fs) and background (%.2fs) tracks...", 
                len(vocal)/1000, len(background)/1000)
    
    background = background - 8
    vocal = vocal + 6
    if len(background) < len(vocal):
        silence_duration = len(vocal) - len(background)
        logger.debug("Background shorter than vocal, adding %dms silence", silence_duration)
        background = background.append(AudioSegment.silent(duration=silence_duration))
    mixed = background.overlay(vocal, position=0)
    normalized = mixed.normalize()
    logger.info("Tracks mixed successfully (total length: %.2f seconds)", len(normalized)/1000)
    return normalized


def generate_song(
    output_file: str = "song.mp3",
    lyrics_text: str = "كلمات الأغنية",
    style: str = DEFAULT_STYLE,
    tempo_override: int | None = None,
) -> str:
    """Create an MP3 song from lyrics and style."""
    logger.info("=" * 70)
    logger.info("SONG GENERATION REQUEST RECEIVED")
    logger.info("=" * 70)
    logger.info("Input parameters:")
    logger.info("  - Lyrics length: %d characters", len(lyrics_text))
    logger.info("  - Style: %s", style)
    logger.info("  - Tempo override: %s BPM", tempo_override or "None (use style default)")
    logger.info("  - Output file: %s", output_file)
    
    try:
        initialize_models()
        style = validate_style(style)
        tempo = validate_tempo(tempo_override)
        lyrics_text = lyrics_text.strip() or "نَشامى… نَشامى… هايبَه وگُوَّه"

        logger.info("-" * 70)
        logger.info("STEP 1: Creating vocal track...")
        vocal_segment = create_vocal_track(lyrics_text, style, tempo)
        
        background_duration = max(len(vocal_segment), 15000)
        logger.info("-" * 70)
        logger.info("STEP 2: Creating background track...")
        background_segment = create_background_track(style, background_duration, tempo)
        
        logger.info("-" * 70)
        logger.info("STEP 3: Mixing tracks...")
        final_song = mix_tracks(vocal_segment, background_segment)

        logger.info("-" * 70)
        logger.info("STEP 4: Exporting to MP3...")
        try:
            final_song.export(output_file, format="mp3", bitrate="192k")
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            logger.info("MP3 exported successfully")
            logger.info("  - File: %s", output_file)
            logger.info("  - Size: %.2f MB", file_size_mb)
        except Exception as exc:
            logger.error("Failed to export MP3: %s", exc, exc_info=True)
            raise
        
        logger.info("=" * 70)
        logger.info("SONG GENERATION COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)
        return output_file
        
    except Exception as exc:
        logger.error("=" * 70)
        logger.error("SONG GENERATION FAILED")
        logger.error("Error: %s", exc, exc_info=True)
        logger.error("=" * 70)
        raise


if __name__ == "__main__":
    result = generate_song(
        output_file="song.mp3",
        lyrics_text="نَشامى… نَشامى… هايبَه وگُوَّه",
        style="حماسي",
    )
    print(f"تم إنشاء ملف MP3 بنجاح: {result}")
