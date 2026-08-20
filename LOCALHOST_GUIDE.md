# 🌐 LOCALHOST ACCESS GUIDE

## Quick Start

### Option 1: Easy Launcher (Recommended)

```bash
python run_localhost.py
```

Then choose:
- `1` → Streamlit UI (http://localhost:8501)
- `2` → Gradio UI (http://localhost:7860)

---

## Option 2: Direct Commands

### Streamlit UI
```bash
streamlit run app.py
```

**Opens automatically:** http://localhost:8501

**Features:**
- ✅ Simple, beginner-friendly interface
- ✅ Upload video directly
- ✅ Real-time processing feedback
- ✅ Download dubbed video
- ✅ Works on local network

### Gradio UI
```bash
python gradio_app.py
```

**Opens automatically:** http://localhost:7860

**Features:**
- ✅ Professional interface
- ✅ Shareable public links
- ✅ Production-ready
- ✅ Mobile-friendly
- ✅ Easy deployment

---

## 📍 LOCAL HOST ADDRESSES

### Accessing from Same Computer
```
Streamlit:  http://localhost:8501
Gradio:     http://localhost:7860

OR

Streamlit:  http://127.0.0.1:8501
Gradio:     http://127.0.0.1:7860
```

### Accessing from Another Computer on Network

**Find your IP address:**

```bash
# Linux/macOS
ifconfig | grep "inet "

# Windows
ipconfig
```

**Then access from another computer:**
```
http://<your-ip>:8501    (Streamlit)
http://<your-ip>:7860    (Gradio)
```

**Example:**
```
If your IP is 192.168.1.100:
  http://192.168.1.100:8501
  http://192.168.1.100:7860
```

---

## 🎬 HOW TO USE

### Streamlit Workflow

1. **Upload Video**
   - Click "Browse files"
   - Select MP4, MOV, or AVI

2. **Optional: Voice Reference**
   - Upload separate audio file (optional)

3. **Select Language**
   - Choose from 50+ languages
   - Default: Hindi

4. **Run Pipeline**
   - Click "🚀 Run dubbing pipeline"
   - Wait for processing

5. **Download**
   - Click "⬇️ Download dubbed video"
   - Video will have synced lips and audio

### Gradio Workflow

1. **Same steps as Streamlit**
2. **Additional Features:**
   - Share link (public access)
   - Embed in websites
   - API access
   - Mobile app

---

## ⏱️ PROCESSING TIME

| Video Length | GPU (CUDA) | CPU |
|---|---|---|
| 30 seconds | 2-3 min | 10-15 min |
| 1 minute | 3-5 min | 15-25 min |
| 2 minutes | 5-10 min | 25-40 min |
| 5 minutes | 10-20 min | 40-60 min |

**Tips:**
- GPU is **10x faster** than CPU
- Smaller model sizes are faster
- Shorter videos process quicker

---

## 🔧 TROUBLESHOOTING

### Port Already in Use

```bash
# Change Streamlit port
streamlit run app.py --server.port 8502

# Change Gradio port
PORTS=7861 python gradio_app.py
```

### Can't Access from Network

```bash
# Allow network access in Streamlit
streamlit run app.py --server.address 0.0.0.0
```

### Slow Processing

**Check GPU:**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**If False, use CPU:**
- Edit `config.yaml`
- Change `device: "cpu"`

### Out of Memory

```yaml
# In config.yaml
device: "cpu"  # Switch to CPU

# Or reduce model size
transcription:
  model_size: "small"  # Instead of "medium"
```

### Module Not Found

```bash
# Make sure venv is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🌐 NETWORK CONFIGURATION

### Access from Same WiFi Network

1. **Find your local IP:**
   ```bash
   # Linux/macOS
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Windows
   ipconfig
   # Look for IPv4 Address (usually 192.168.x.x)
   ```

2. **Access from other device:**
   ```
   http://192.168.1.100:8501  (replace 100 with your IP)
   ```

### Access from Internet (Gradio)

**Gradio automatically creates shareable links:**

```
🔗 Share link: https://abc123.gradio.live

This link works from anywhere in the world!
It expires after 72 hours.
```

---

## 📊 MONITORING

### Streamlit Console Output
```
Network URL: http://192.168.1.100:8501
External URL: http://203.0.113.42:8501  (if accessible from internet)
You can now view your Streamlit app in your browser.
```

### Gradio Console Output
```
Running on local URL:  http://127.0.0.1:7860
Running on share URL: https://abc123.gradio.live
Share this URL with anyone to get a public link to your app!
```

---

## 🔒 SECURITY NOTES

### Protect Your Application

```bash
# Only allow local access (default)
streamlit run app.py

# Allow network access (use with caution)
streamlit run app.py --server.address 0.0.0.0
```

### Keep Private
- Don't share gradio.live links publicly
- Use VPN for remote access
- Set up authentication for production

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Hugging Face Spaces (Free)

```bash
# Push to GitHub
git push origin main

# Create Space on Hugging Face
# Connect to GitHub repo
# Automatic deployment!
```

### Option 2: AWS

```bash
# EC2 instance
# Install dependencies
# Run app.py or gradio_app.py
```

### Option 3: Google Cloud

```bash
# Cloud Run
# Cloud Compute Engine
# Follow Google docs
```

---

## 📞 SUPPORT

- **Docs:** INSTALLATION_COMPLETE.md, QUICKSTART.md
- **GitHub:** https://github.com/devika10dhoke/VOICE-CLONING-LIP-SYNCHRONIZATION-BY-USING-GEN--AI
- **Issues:** Report on GitHub Issues page

---

## ✅ QUICK CHECKLIST

- [ ] Repository cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ffmpeg installed
- [ ] Wav2Lip weights downloaded (optional for lip-sync)
- [ ] Run `python run_localhost.py` or `streamlit run app.py`
- [ ] Open browser to http://localhost:8501 or :7860
- [ ] Upload video and test!

---

**Happy dubbing! 🎬**
