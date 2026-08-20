# Architecture

## Overview

The pipeline is a linear, five-stage flow. Each stage is a standalone module with its own CLI entry point, and communicates with the next stage through file-based artifacts (JSON transcripts, WAV audio, MP4 video). This keeps stages independently testable and swappable.

## Stages

### 1. Video Analysis (`src/video_analysis.py`)
- Extracts metadata (fps, resolution, duration)
- Extracts the audio track via ffmpeg
- Samples frames at a configurable rate
- Detects the primary face bounding box per frame (MediaPipe or `face_alignment`)
- Output: `analysis_report.json`, sampled frames, `source_audio.wav`

### 2. Transcription (`src/transcription.py`)
- Runs OpenAI Whisper on the extracted audio
- Produces segment-level text with start/end timestamps
- Output: `transcript.json`

### 3. Translation (`src/translation.py`)
- Translates each transcript segment using NLLB-200 (swappable for any HF seq2seq MT model / MarianMT)
- Preserves segment timestamps for later re-synchronization
- Output: `translated_transcript.json`

### 4. Voice Cloning (`src/voice_cloning.py`)
- Uses Coqui XTTS-v2 for few-shot, speaker-conditioned multilingual TTS
- Takes a short reference clip of the target speaker's voice (default: the video's own source audio) and synthesizes the translated text in that voice
- Output: `cloned_voice.wav`

### 5. Lip Synchronization (`src/lip_sync.py`)
- Wraps Wav2Lip (GAN-based) to regenerate the mouth region of the source video frames so they match the new audio track's phonemes/timing
- Output: final dubbed `.mp4`

## Design Decisions

- **File-based inter-stage contracts** rather than in-memory objects, so any stage can be re-run, cached, or replaced without touching the others.
- **Config-driven** (`config/config.yaml`): model choices, languages, and device are all externalized — no hardcoded model names in pipeline logic.
- **Segment-level granularity**: translation and TTS operate per-segment (not on the full transcript as one blob) so that timing stays closer to the original per-sentence pacing, which materially helps lip-sync quality.

## Known Limitations

- Whisper, XTTS, and Wav2Lip are all GPU-hungry; CPU inference works but is slow (minutes per short clip).
- Wav2Lip performs best on front-facing, single-speaker video; multi-speaker or heavy head-turn footage degrades sync quality.
- Voice cloning quality depends heavily on reference clip quality (clean audio, 6+ seconds, minimal background noise).
- Segment-level TTS durations won't always exactly match the original segment length — a duration-matching/time-stretch step (not yet implemented) would further improve sync for strict timing requirements.

## Possible Extensions

- Duration-aware TTS (adjust synthesis speed to match original segment length before lip-sync)
- Multi-speaker diarization + per-speaker voice cloning
- Swap Wav2Lip for a diffusion-based lip-sync model for higher fidelity
- Dockerfile + docker-compose for reproducible GPU deployment
