# 🚀 Quick Start Guide — Complete Setup & Run

## One-Command Setup

### 🐧 **Linux / macOS**
```bash
bash setup_and_run.sh
```

### 🪟 **Windows**
```cmd
setup_and_run.bat
```

---

## What the Setup Script Does

The automated scripts handle **all** the heavy lifting:

✅ **Checks Python version** (requires 3.9+)  
✅ **Creates & activates virtual environment**  
✅ **Installs all dependencies** (takes 2-5 minutes on first run)  
✅ **Creates required directories** (weights, outputs, temp, assets)  
✅ **Verifies ffmpeg installation**  
✅ **Checks for Wav2Lip weights** (with download link if missing)  
✅ **Launches your choice of UI** (Streamlit or Gradio)  

---

## Expected Output

When you run the setup script, you'll see:

```
========================================================
🎙️  VOICE CLONING & LIP-SYNC SETUP & RUN
========================================================

[Step 1/6] Checking Python version...
✓ Python 3.11.0 found

[Step 2/6] Setting up virtual environment...
✓ Virtual environment activated

[Step 3/6] Installing dependencies...
Installing project dependencies (this may take 2-5 minutes)...
✓ Dependencies installed

[Step 4/6] Creating necessary directories...
✓ Directories created

[Step 5/6] Checking Wav2Lip weights...
⚠️  WARNING: Wav2Lip weights not found!
Please download wav2lip_gan.pth from: https://github.com/Rudrabha/Wav2Lip
And place it in: weights/wav2lip_gan.pth

[Step 6/6] Checking ffmpeg installation...
✓ ffmpeg found

========================================================
✓ Setup Complete!
========================================================

Choose which interface to launch:

  1) Streamlit UI (Simpler, recommended for beginners)
  2) Gradio UI (More flexible, easy to deploy to Hugging Face)
  3) Exit setup without launching

Enter your choice (1-3):
```

---

## After Setup �� Manual Launch

If you exit without launching, you can manually start the app:

### **Streamlit** (Simple Web UI)
```bash
streamlit run app.py
```
**Opens:** http://localhost:8501

### **Gradio** (Flexible Web UI, Deploy-friendly)
```bash
python gradio_app.py
```
**Opens:** http://localhost:7860

---

## Troubleshooting

### ❌ "Python not found"
- Install Python 3.9+ from https://www.python.org/
- Make sure to check **"Add Python to PATH"** during installation
- Restart your terminal/command prompt

### ❌ "ffmpeg not found"
```bash
# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

### ❌ "Wav2Lip weights not found"
1. Download `wav2lip_gan.pth` from: https://github.com/Rudrabha/Wav2Lip
2. Place it in: `weights/wav2lip_gan.pth`
3. Restart the application

### ❌ Permission Denied (Linux/macOS)
```bash
chmod +x setup_and_run.sh
bash setup_and_run.sh
```

### ❌ Long Installation Time
- First run downloads **several GB** of model weights (Whisper, NLLB, XTTS-v2)
- Subsequent runs are much faster
- Consider using a GPU for faster inference (CUDA 11.8+)

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| **Python** | 3.9 or higher |
| **RAM** | 8 GB minimum (16 GB recommended) |
| **GPU** | Optional but **strongly recommended** (CUDA 11.8+) |
| **Disk** | ~5-10 GB (for models + outputs) |
| **ffmpeg** | Required for video processing |

---

## Using the Web Interface

### **Step 1: Upload Video**
- Click "Upload source video"
- Select MP4, MOV, or AVI file

### **Step 2: (Optional) Voice Reference**
- Upload a separate voice clip if you want a specific voice model
- Leave blank to use the speaker's original voice from the video

### **Step 3: Choose Target Language**
- Hindi, French, Spanish, German, Japanese, etc.
- 50+ languages supported!

### **Step 4: Run Pipeline**
- Click 🚀 **"Run dubbing pipeline"**
- Wait for processing (takes longer on CPU)

### **Step 5: Download**
- Once complete, download your dubbed video
- Video will have:
  - ✓ New audio in target language
  - ✓ Voice cloned from original speaker
  - ✓ Lips synchronized to match new audio

---

## Command-Line Usage (Advanced)

### **Full Pipeline**
```bash
python -m src.pipeline \\
    --input path/to/video.mp4 \\
    --target-lang hi \\
    --output path/to/output_hindi.mp4
```

### **Individual Stages**
```bash
# Video Analysis
python -m src.video_analysis --input video.mp4

# Transcription
python -m src.transcription --input video.mp4

# Translation
python -m src.translation --text "Hello, how are you?" --target-lang fr

# Voice Cloning
python -m src.voice_cloning --text "Bonjour" --speaker-audio voice_ref.wav

# Lip Sync
python -m src.lip_sync --video video.mp4 --audio output.wav
```

---

## Configuration

Edit `config.yaml` to customize:

```yaml
device: "cuda"           # "cuda" or "cpu"

video_analysis:
  fps_sample_rate: 25    # frames per second to process

transcription:
  model_size: "medium"   # tiny | base | small | medium | large-v3

translation:
  model_name: "facebook/nllb-200-distilled-600M"

voice_cloning:
  model_name: "tts_models/multilingual/multi-dataset/xtts_v2"
  target_language: "hi"

lip_sync:
  checkpoint_path: "weights/wav2lip_gan.pth"
```

---

## ⚠️ Ethical Use Notice

Voice cloning and lip-sync technology can be misused for impersonation or deepfakes.

**This project is for LEGITIMATE use only:**
- ✅ Video dubbing & localization
- ✅ Accessibility features
- ✅ Research & development
- ✅ Entertainment (with consent)

**Always:**
- 🔒 Obtain **explicit consent** before cloning anyone's voice
- 📢 **Disclose** when sharing synthetic/dubbed media
- ⚖️ Follow **local laws** regarding deepfakes

---

## Support & Issues

- 📖 Full docs: [ARCHITECTURE.md](ARCHITECTURE.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/devika10dhoke/VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI/issues)
- 📜 License: [MIT](LICENSE)

---

**Happy dubbing! 🎬**