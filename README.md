# 🎙️ Voice Cloning & Lip Synchronization using Gen-AI

An advanced AI-driven pipeline for **video analysis, multilingual translation, voice cloning, and precise visual lip-sync** — enabling seamless, natural-sounding cross-language dubbing of video content.

> Turn any speaker's video into a naturally dubbed version in another language, in **their own cloned voice**, with lips that match the new audio.

---

## ✨ Features

- 🎞️ **Video Analysis** — face detection, scene/frame extraction, source audio isolation
- 📝 **Speech-to-Text** — high-accuracy multilingual transcription (Whisper)
- 🌐 **Neural Machine Translation** — context-aware translation across 50+ languages
- 🗣️ **Voice Cloning / TTS** — few-shot speaker-conditioned voice synthesis (Coqui XTTS-v2)
- 👄 **Lip Synchronization** — GAN-based visual dubbing so mouth movement matches the new audio (Wav2Lip)
- 🔄 **End-to-end Pipeline** — single command from source video → translated, lip-synced output
- 🖥️ **Simple UI** — Streamlit demo app for non-technical use
- ⚙️ **Modular Design** — swap any stage (ASR / MT / TTS / lip-sync model) independently

---

## 🏗️ Architecture

```
                ┌────────────────┐
   Input Video  │  Video Analysis│  → frames, face crops, audio track
   ───────────► │   (OpenCV/     │
                │   ffmpeg)      │
                └───────┬────────┘
                        ▼
                ┌────────────────┐
                │  Transcription │  → source-language text + timestamps
                │   (Whisper)    │
                └───────┬────────┘
                        ▼
                ┌────────────────┐
                │  Translation   │  → target-language text
                │  (NLLB / MT)   │
                └───────┬────────┘
                        ▼
                ┌────────────────┐
                │ Voice Cloning  │  → cloned-voice audio in target language
                │  (Coqui XTTS)  │
                └───────┬────────┘
                        ▼
                ┌────────────────┐
                │  Lip Sync      │  → final dubbed video with synced lips
                │  (Wav2Lip)     │
                └───────┬────────┘
                        ▼
                  Output Video
```

Each stage lives in its own module under `src/` and communicates through simple file-based artifacts (`.wav`, `.json`, `.mp4`), so any stage can be replaced or run standalone.

---

## 📁 Project Structure

```
voice-cloning-lipsync/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── app.py                     # Streamlit demo UI
├── config/
│   └── config.yaml            # model + pipeline configuration
├── src/
│   ├── __init__.py
│   ├── video_analysis.py      # frame/audio/face extraction
│   ├── transcription.py       # Whisper-based ASR
│   ├── translation.py         # multilingual MT
│   ├── voice_cloning.py       # speaker-conditioned TTS
│   ├── lip_sync.py            # Wav2Lip wrapper
│   ├── pipeline.py            # orchestrates the full flow
│   └── utils.py                # shared helpers (logging, io, ffmpeg wrappers)
├── tests/
│   └── test_pipeline.py
├── docs/
│   └── ARCHITECTURE.md
├── assets/sample/              # sample input/output for demo
└── .github/workflows/ci.yml    # lint + test CI
```

---

## ⚙️ Setup

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/voice-cloning-lipsync.git
cd voice-cloning-lipsync
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. External dependencies

- **ffmpeg** must be installed and on your PATH (`sudo apt install ffmpeg` / `brew install ffmpeg`)
- **Wav2Lip weights** — download `wav2lip_gan.pth` from the [official Wav2Lip repo](https://github.com/Rudrabha/Wav2Lip) and place it in `weights/`
- **GPU strongly recommended** (CUDA 11.8+) for Whisper, XTTS and Wav2Lip inference speed

### 3. Configure

Edit `config/config.yaml` to set source/target languages, model sizes, and device (`cpu`/`cuda`).

---

## 🚀 Usage

### CLI — full pipeline

```bash
python -m src.pipeline \
    --input assets/sample/input.mp4 \
    --target-lang hi \
    --output assets/sample/output_hindi.mp4
```

### Run a single stage

```bash
python -m src.transcription --input assets/sample/input.mp4
python -m src.translation --text "Hello, how are you?" --target-lang fr
python -m src.voice_cloning --text "Bonjour" --speaker-audio assets/sample/voice_ref.wav
python -m src.lip_sync --video assets/sample/input.mp4 --audio output.wav
```

### Web UI

```bash
streamlit run app.py
```

---

## 🧩 Tech Stack

| Stage | Model / Library |
|---|---|
| Video/Audio I/O | `ffmpeg-python`, `opencv-python` |
| Face detection | `face_alignment` / `mediapipe` |
| Transcription | `openai-whisper` |
| Translation | `transformers` (NLLB-200 / MarianMT) |
| Voice Cloning | `TTS` (Coqui XTTS-v2) |
| Lip Sync | `Wav2Lip` (GAN-based) |
| UI | `streamlit` |

---

## 🗺️ Roadmap

- [ ] Batch processing for multi-speaker videos
- [ ] Real-time streaming mode
- [ ] Emotion-preserving voice cloning
- [ ] Support for additional lip-sync backbones (e.g. video diffusion models)
- [ ] Dockerized deployment

---

## ⚠️ Ethical Use Notice

Voice cloning and lip-sync technology can be misused for impersonation or deepfakes. This project is intended for **legitimate localization, dubbing, accessibility, and research use only**. Always obtain explicit consent from the speaker before cloning their voice or likeness, and disclose synthetic media where required by law or platform policy.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
