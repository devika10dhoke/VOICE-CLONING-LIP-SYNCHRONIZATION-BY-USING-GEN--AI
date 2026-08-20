#!/bin/bash

# =========================================================
# VOICE CLONING & LIP-SYNC SETUP & RUN SCRIPT
# =========================================================
# This script automates:
# 1. Environment setup
# 2. Dependency installation
# 3. Configuration
# 4. Web application launch
# =========================================================

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================================${NC}"
echo -e "${BLUE}🎙️  VOICE CLONING & LIP-SYNC SETUP & RUN${NC}"
echo -e "${BLUE}========================================================${NC}\n"

# =========================================================
# Step 1: Check Python version
# =========================================================
echo -e "${YELLOW}[Step 1/6] Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}\n"

# =========================================================
# Step 2: Create virtual environment
# =========================================================
echo -e "${YELLOW}[Step 2/6] Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# =========================================================
# Step 3: Install dependencies
# =========================================================
echo -e "${YELLOW}[Step 3/6] Installing dependencies...${NC}"
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

echo "Installing project dependencies (this may take 2-5 minutes)..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# =========================================================
# Step 4: Create necessary directories
# =========================================================
echo -e "${YELLOW}[Step 4/6] Creating necessary directories...${NC}"
mkdir -p weights
mkdir -p outputs
mkdir -p temp
mkdir -p assets/sample
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}\n"

# =========================================================
# Step 5: Check for Wav2Lip weights
# =========================================================
echo -e "${YELLOW}[Step 5/6] Checking Wav2Lip weights...${NC}"
if [ ! -f "weights/wav2lip_gan.pth" ]; then
    echo -e "${RED}⚠️  WARNING: Wav2Lip weights not found!${NC}"
    echo -e "${YELLOW}Please download wav2lip_gan.pth from:${NC}"
    echo -e "${BLUE}https://github.com/Rudrabha/Wav2Lip${NC}"
    echo -e "${YELLOW}And place it in: weights/wav2lip_gan.pth${NC}\n"
    echo -e "${YELLOW}The application will still start, but lip-sync will fail until weights are added.${NC}\n"
else
    echo -e "${GREEN}✓ Wav2Lip weights found${NC}\n"
fi

# =========================================================
# Step 6: Check for ffmpeg
# =========================================================
echo -e "${YELLOW}[Step 6/6] Checking ffmpeg installation...${NC}"
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1)
    echo -e "${GREEN}✓ ffmpeg found: ${FFMPEG_VERSION}${NC}\n"
else
    echo -e "${RED}✗ ffmpeg not found!${NC}"
    echo -e "${YELLOW}Please install ffmpeg:${NC}"
    echo -e "${BLUE}Linux: sudo apt install ffmpeg${NC}"
    echo -e "${BLUE}macOS: brew install ffmpeg${NC}"
    echo -e "${BLUE}Windows: choco install ffmpeg${NC}"
    exit 1
fi

# =========================================================
# Select and Launch App
# =========================================================
echo -e "${GREEN}========================================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}========================================================\n${NC}"

echo -e "${BLUE}Choose which interface to launch:${NC}\n"
echo "  1) Streamlit UI (Simpler, recommended for beginners)"
echo "  2) Gradio UI (More flexible, easy to deploy to Hugging Face)"
echo "  3) Exit setup without launching"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo -e "\n${YELLOW}Launching Streamlit app...${NC}\n"
        echo -e "${BLUE}The app will open in your browser at http://localhost:8501${NC}\n"
        streamlit run app.py
        ;;
    2)
        echo -e "\n${YELLOW}Launching Gradio app...${NC}\n"
        echo -e "${BLUE}The app will open in your browser at http://localhost:7860${NC}\n"
        python gradio_app.py
        ;;
    3)
        echo -e "\n${YELLOW}Setup complete. You can manually launch:${NC}\n"
        echo -e "${BLUE}Streamlit:  streamlit run app.py${NC}"
        echo -e "${BLUE}Gradio:     python gradio_app.py${NC}\n"
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac
