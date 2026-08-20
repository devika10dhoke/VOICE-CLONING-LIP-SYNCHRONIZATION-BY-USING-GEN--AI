# 🚀 COMPLETE LOCALHOST SETUP & RUN GUIDE

## ✅ YOU ARE READY TO GO!

Follow these exact steps to run your Voice Cloning & Lip-Sync application locally.

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### **STEP 1: Clone Repository**

```bash
git clone https://github.com/devika10dhoke/VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI.git

cd VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI
```

**Output:**
```
Cloning into 'VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI'...
remote: Enumerating objects: 25, done.
remote: Counting objects: 100% (25/25), done.
remote: Compressing objects: 100% (18/18), done.
remote: Receiving objects: 100% (25/25), 145.32 KiB | 2.5 MiB/s, done.
remote: Resolving deltas: 100% (5/5), done.
```

✅ **Check:** You should be in the project directory
```bash
ls  # or 'dir' on Windows
# Should show: app.py, config.yaml, requirements.txt, setup_and_run.sh, etc.
```

---

### **STEP 2: Create Virtual Environment**

#### **Linux/macOS:**
```bash
python3 -m venv venv

source venv/bin/activate
```

#### **Windows:**
```bash
python -m venv venv

venv\Scripts\activate
```

**Output (after activation):**
```
(venv) $ _  # You'll see (venv) prefix in your terminal
```

✅ **Check:** Type `python --version` - should show Python 3.9+

---

### **STEP 3: Install Dependencies**

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

**This will take 3-5 minutes. You'll see:**
```
Collecting numpy>=1.24.0
Collecting scipy>=1.11.0
Collecting tqdm>=4.66.0
...
Successfully installed numpy scipy torch transformers ...
```

✅ **Check:** No error messages at the end

---

### **STEP 4: Install System Dependencies**

#### **Check if ffmpeg is installed:**
```bash
ffmpeg -version
```

#### **If not installed, install it:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
# OR download from https://ffmpeg.org/download.html
```

✅ **Check:** Run `ffmpeg -version` again

---

### **STEP 5: Create Required Directories**

```bash
mkdir -p weights outputs temp assets/sample logs
```

**Or manually create:**
- `weights/` - for model weights
- `outputs/` - for output videos
- `temp/` - for temporary files
- `assets/sample/` - for sample videos
- `logs/` - for log files

✅ **Check:**
```bash
ls -la  # Should show all directories
```

---

### **STEP 6: Download Wav2Lip Weights (Optional but Recommended)**

**Note:** Lip-sync won't work without this

```bash
cd weights

# Download wav2lip_gan.pth from:
# https://github.com/Rudrabha/Wav2Lip

# Place the file here as: wav2lip_gan.pth

cd ..
```

✅ **Check:**
```bash
ls weights/wav2lip_gan.pth  # Should exist
```

---

### **STEP 7: Run the Application**

#### **Option A: Using Easy Launcher (Recommended)**

```bash
python run_localhost.py
```

**You'll see:**
```
🎙️  VOICE CLONING & LIP-SYNC LOCAL HOST LAUNCHER
✅ Python 3.11.0 detected
✅ Streamlit installed
✅ Gradio installed

============================================================
🚀 VOICE CLONING & LIP-SYNC - LOCAL HOST
============================================================

📋 AVAILABLE SERVERS:

  1) Streamlit UI (Recommended for beginners)
     └─ http://localhost:8501
     └─ Simple, interactive interface
     └─ Real-time feedback

  2) Gradio UI (Deploy-ready)
     └─ http://localhost:7860
     └─ Shareable links
     └─ Production-ready

  3) View Documentation
  4) Exit

============================================================

Enter your choice (1-4):
```

**Choose: Press `1` for Streamlit or `2` for Gradio**

---

#### **Option B: Direct Launch**

**Streamlit:**
```bash
streamlit run app.py
```

**Gradio:**
```bash
python gradio_app.py
```

---

### **STEP 8: Access in Browser**

#### **Streamlit:**
```
http://localhost:8501
```

**You'll see:**
```
🎙️ Voice Cloning & Lip-Sync Studio

Upload a video, choose a target language, and generate a
naturally dubbed, lip-synced version in the speaker's own
cloned voice.

⚙️ Settings (Sidebar)
  - Config file: config/config.yaml
  - Target language: hi (Hindi)
  
[Upload source video] ← Click here
[Upload voice reference (optional)] ← Or here
[🚀 Run dubbing pipeline] ← Then click here
```

#### **Gradio:**
```
http://localhost:7860
```

**You'll see:**
```
🎙️ Voice Cloning & Lip-Sync Studio

Upload a video, choose a target language, and get back a
naturally dubbed version in the speaker's own cloned voice,
with lips synced to the new audio.

[Source video upload area]
[Optional: separate voice reference clip]
[Target language: Hindi ▼]
[🚀 Run dubbing pipeline]
```

---

## 🎬 HOW TO USE THE INTERFACE

### **Step 1: Upload Video**
- Click the upload area
- Select a video file (MP4, MOV, or AVI)
- Max recommended: 5 minutes

### **Step 2: (Optional) Upload Voice Reference**
- If you want a specific voice, upload a voice clip
- If left empty, uses the original speaker's voice

### **Step 3: Select Target Language**
- Click the language dropdown
- Choose from 50+ languages
- Default: Hindi

**Available languages:**
- Hindi (hi)
- French (fr)
- Spanish (es)
- German (de)
- Japanese (ja)
- Mandarin (zh-cn)
- Arabic (ar)
- Portuguese (pt)
- Russian (ru)
- Korean (ko)
- Italian (it)
- Turkish (tr)
- And 40+ more...

### **Step 4: Run Pipeline**
- Click "🚀 Run dubbing pipeline"
- Wait for processing

**You'll see progress:**
```
=== Stage 1/5: Video analysis ===
[INFO] Extracting audio track...
[INFO] Extracted 150 frames

=== Stage 2/5: Transcription ===
[INFO] Loading Whisper model...
[INFO] Transcribing audio...

=== Stage 3/5: Translation ===
[INFO] Translating text...

=== Stage 4/5: Voice cloning ===
[INFO] Loading TTS model...
[INFO] Synthesizing speech...

=== Stage 5/5: Lip synchronization ===
[INFO] Running Wav2Lip...
[INFO] Lip-synced video written to outputs/output_hindi.mp4

Pipeline complete!
```

### **Step 5: Download**
- Click the download button
- Save the dubbed video
- Play and enjoy!

---

## ⏱️ EXPECTED PROCESSING TIME

```
 Video Length  |  GPU (CUDA)  |  CPU
  30 seconds   |   2-3 min    | 10-15 min
  1 minute     |   3-5 min    | 15-25 min
  2 minutes    |   5-10 min   | 25-40 min
  5 minutes    |  10-20 min   | 40-60 min
```

**Tips:**
- GPU is 10x faster than CPU
- Shorter videos process quicker
- First run is slower (downloads models)

---

## 🌍 ACCESS FROM ANOTHER COMPUTER

### **Find Your IP:**

**Linux/macOS:**
```bash
ifconfig | grep "inet "
```

**Windows:**
```cmd
ipconfig
```

Look for: `192.168.1.XXX`

### **Access from Other Device:**

If your IP is `192.168.1.100`:

```
http://192.168.1.100:8501   (Streamlit)
http://192.168.1.100:7860   (Gradio)
```

---

## 🛠️ TROUBLESHOOTING

### ❌ "Port already in use"

**Solution:**
```bash
# For Streamlit
streamlit run app.py --server.port 8502

# For Gradio
PORTS=7861 python gradio_app.py
```

### ❌ "ModuleNotFoundError: No module named 'src'"

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Make sure you're in correct directory
ls app.py  # Should show the file
```

### ❌ "ffmpeg not found"

**Solution:** Install ffmpeg (see Step 4)

### ❌ "CUDA out of memory"

**Solution:**
```yaml
# Edit config.yaml
device: "cpu"  # Use CPU instead
```

### ❌ "Wav2Lip checkpoint not found"

**Solution:** Download weights (see Step 6)

### ❌ "Slow processing"

**Solution:**
```yaml
# Edit config.yaml
transcription:
  model_size: "small"  # Instead of "medium"

device: "cuda"  # Use GPU
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] ffmpeg installed
- [ ] Directories created
- [ ] Wav2Lip weights downloaded (optional)
- [ ] Application started (python run_localhost.py or streamlit run app.py)
- [ ] Browser opens to localhost:8501 or :7860
- [ ] Can upload video
- [ ] Can select language
- [ ] Pipeline runs successfully
- [ ] Can download output video

---

## 🎯 QUICK REFERENCE

```bash
# Clone
git clone https://github.com/devika10dhoke/VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI.git
cd VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI

# Setup
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create directories
mkdir -p weights outputs temp assets/sample logs

# Run
python run_localhost.py
# OR
streamlit run app.py
# OR
python gradio_app.py

# Access
http://localhost:8501   (Streamlit)
http://localhost:7860   (Gradio)
```

---

## 📱 ACCESS URLS

**Local Computer:**
```
http://localhost:8501
http://127.0.0.1:8501
```

**Same Network:**
```
http://192.168.1.100:8501  (replace 100 with your IP)
```

**Gradio Public Link (temporary):**
```
https://abc123def456.gradio.live  (shown after start)
```

---

## 📞 SUPPORT

- **Documentation:** INSTALLATION_COMPLETE.md, QUICKSTART.md, LOCALHOST_GUIDE.md
- **GitHub:** https://github.com/devika10dhoke/VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI
- **Issues:** Report on GitHub Issues page

---

## ✨ YOU'RE READY!

**Everything is set up and ready to run.**

**Next step:** Execute `python run_localhost.py` 🚀

---

**Last Updated:** 2026-08-20  
**Status:** ✅ Complete & Ready to Use
