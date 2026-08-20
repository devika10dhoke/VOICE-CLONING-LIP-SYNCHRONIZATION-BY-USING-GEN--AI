"""
Voice Cloning & Lip Synchronization using Gen-AI
=================================================

Modular pipeline package.

Modules
-------
video_analysis   : frame/audio/face extraction from source video
transcription    : speech-to-text (Whisper)
translation      : multilingual machine translation
voice_cloning    : speaker-conditioned text-to-speech
lip_sync         : Wav2Lip-based visual dubbing
pipeline         : orchestrates the end-to-end flow
utils            : shared helpers
"""

__version__ = "0.1.0"
