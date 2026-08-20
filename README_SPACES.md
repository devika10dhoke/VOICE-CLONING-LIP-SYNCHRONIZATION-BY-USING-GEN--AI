---
title: Voice Cloning & Lip-Sync Studio
emoji: 🎙️
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: "4.44.0"
app_file: gradio_app.py
pinned: false
license: mit
---

# Voice Cloning & Lip-Sync Studio

Upload a video, pick a target language, and get back a dubbed version in
the speaker's own cloned voice with lips synced to the new audio.

See the main [README.md](README.md) for the full pipeline architecture,
local setup, and CLI usage. This Space runs the same pipeline through
`gradio_app.py`.

## Before deploying

1. This Space needs a **GPU hardware tier** (Settings → Hardware) —
   Whisper, XTTS-v2, and Wav2Lip are all too slow on CPU-only tiers for
   interactive use.
2. Upload the Wav2Lip checkpoint (`wav2lip_gan.pth`) into `weights/` in
   this Space's file browser, or add a download step to `packages.txt` /
   a startup script — it is not bundled in this repo (see
   `weights/README.md`).
3. `ffmpeg` is required at the OS level — add a `packages.txt` file
   containing the line `ffmpeg` to this Space so the Spaces builder
   installs it automatically.
