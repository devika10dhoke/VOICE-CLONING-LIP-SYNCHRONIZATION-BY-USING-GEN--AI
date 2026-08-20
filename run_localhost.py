#!/usr/bin/env python3
"""
Local Hosting Guide for Voice Cloning & Lip-Sync Application
=============================================================

This script demonstrates how to run and access the application locally.
"""

import subprocess
import time
import webbrowser
import sys
from pathlib import Path

def check_python():
    """Verify Python version."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_dependencies():
    """Check if key dependencies are installed."""
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        print("❌ Streamlit not installed. Run: pip install streamlit")
        return False
    
    try:
        import gradio
        print("✅ Gradio installed")
    except ImportError:
        print("⚠️  Gradio not installed. Run: pip install gradio")
        return False
    
    return True

def start_streamlit():
    """Start Streamlit server."""
    print("\n" + "="*60)
    print("🎙️  STARTING STREAMLIT SERVER")
    print("="*60)
    print("\n📍 LOCAL ADDRESSES:")
    print("   Local:     http://localhost:8501")
    print("   Network:   http://<your-ip>:8501")
    print("\n💡 SHORTCUT: Press 'C' to quit, 'R' to rerun")
    print("="*60 + "\n")
    
    subprocess.run(["streamlit", "run", "app.py"], cwd=Path.cwd())

def start_gradio():
    """Start Gradio server."""
    print("\n" + "="*60)
    print("🎙️  STARTING GRADIO SERVER")
    print("="*60)
    print("\n📍 LOCAL ADDRESSES:")
    print("   Local:     http://localhost:7860")
    print("   Network:   http://<your-ip>:7860")
    print("   Share Link: (generated after server starts)")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    subprocess.run(["python", "gradio_app.py"], cwd=Path.cwd())

def show_menu():
    """Display menu and get user choice."""
    print("\n" + "="*60)
    print("🚀 VOICE CLONING & LIP-SYNC - LOCAL HOST")
    print("="*60)
    print("\n📋 AVAILABLE SERVERS:\n")
    print("  1) Streamlit UI (Recommended for beginners)")
    print("     └─ http://localhost:8501")
    print("     └─ Simple, interactive interface")
    print("     └─ Real-time feedback")
    print()
    print("  2) Gradio UI (Deploy-ready)")
    print("     └─ http://localhost:7860")
    print("     └─ Shareable links")
    print("     └─ Production-ready")
    print()
    print("  3) View Documentation")
    print("  4) Exit")
    print("\n" + "="*60)
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4")

def show_docs():
    """Show documentation."""
    print("\n" + "="*60)
    print("📖 DOCUMENTATION")
    print("="*60)
    print("""
🎬 WORKFLOW:
  1. Upload video (MP4, MOV, AVI)
  2. Select target language
  3. (Optional) Upload voice reference
  4. Click "Run Pipeline"
  5. Download dubbed video

📊 PROCESSING STAGES:
  Stage 1: Video Analysis
    └─ Extracts frames and audio
  
  Stage 2: Transcription
    └─ Speech-to-text with Whisper
  
  Stage 3: Translation
    └─ Multilingual translation
  
  Stage 4: Voice Cloning
    └─ Speaker-conditioned TTS
  
  Stage 5: Lip Synchronization
    └─ Wav2Lip visual dubbing

⏱️  ESTIMATED TIME:
  - Short video (1-2 min): 5-15 minutes
  - GPU (CUDA): 2-5x faster
  - CPU: 15-30 minutes

🌍 SUPPORTED LANGUAGES:
  Hindi, French, Spanish, German, Japanese, Mandarin,
  Arabic, Portuguese, Russian, Korean, Italian, Turkish,
  and 40+ more

⚙️  CONFIGURATION:
  Edit config.yaml to change:
  - Device (cuda/cpu)
  - Model sizes
  - Languages
  - Processing parameters

🔧 TROUBLESHOOTING:
  Problem: "Module not found: src"
  Solution: Make sure you're in the project root directory

  Problem: "CUDA out of memory"
  Solution: Set device: "cpu" in config.yaml

  Problem: "ffmpeg not found"
  Solution: Install ffmpeg (apt, brew, choco, or manually)

  Problem: "Wav2Lip checkpoint not found"
  Solution: Download weights/wav2lip_gan.pth from:
            https://github.com/Rudrabha/Wav2Lip

📞 SUPPORT:
  - Docs: INSTALLATION_COMPLETE.md, QUICKSTART.md
  - GitHub: https://github.com/devika10dhoke/...
  - Issues: Report on GitHub Issues page
""")
    print("="*60)

def main():
    """Main entry point."""
    print("\n🎙️  VOICE CLONING & LIP-SYNC LOCAL HOST LAUNCHER\n")
    
    # Check environment
    check_python()
    
    if not check_dependencies():
        print("\n⚠️  Some dependencies are missing.")
        print("   Install them with: pip install -r requirements.txt")
        response = input("\n   Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # Main loop
    while True:
        choice = show_menu()
        
        if choice == '1':
            try:
                start_streamlit()
            except KeyboardInterrupt:
                print("\n\n❌ Streamlit server stopped")
            except Exception as e:
                print(f"❌ Error starting Streamlit: {e}")
        
        elif choice == '2':
            try:
                start_gradio()
            except KeyboardInterrupt:
                print("\n\n❌ Gradio server stopped")
            except Exception as e:
                print(f"❌ Error starting Gradio: {e}")
        
        elif choice == '3':
            show_docs()
        
        elif choice == '4':
            print("\n👋 Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...\n")
        sys.exit(0)
