"""
Voice Cloning & Lip Synchronization Package

Modules:
  - pipeline: Main orchestration engine
  - video_analysis: Frame and audio extraction
  - transcription: Speech-to-text with Whisper
  - translation: Multilingual neural translation
  - voice_cloning: Speaker-conditioned TTS with Coqui XTTS-v2
  - lip_sync: Visual dubbing with Wav2Lip
  - utils: Shared utilities and helpers
"""

__version__ = "1.0.0"
__author__ = "devika10dhoke"
__description__ = "An advanced AI-driven solution for video dubbing with voice cloning and lip synchronization"

from src.pipeline import DubbingPipeline
from src.video_analysis import VideoAnalyzer
from src.transcription import Transcriber
from src.translation import Translator
from src.voice_cloning import VoiceCloner
from src.lip_sync import LipSyncer
from src.utils import load_config, get_logger, ensure_dir

__all__ = [
    "DubbingPipeline",
    "VideoAnalyzer",
    "Transcriber",
    "Translator",
    "VoiceCloner",
    "LipSyncer",
    "load_config",
    "get_logger",
    "ensure_dir",
]
