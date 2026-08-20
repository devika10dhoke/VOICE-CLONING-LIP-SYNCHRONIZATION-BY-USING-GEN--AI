# Model Weights

This directory holds large pretrained checkpoints that are NOT committed to git (see `.gitignore`).

Download manually:

- **Wav2Lip GAN checkpoint** (`wav2lip_gan.pth`) — from the official [Wav2Lip repository](https://github.com/Rudrabha/Wav2Lip#getting-the-weights)

Whisper, NLLB, and XTTS-v2 weights are downloaded automatically on first run via their respective libraries (`openai-whisper`, `transformers`, `TTS`) and cached locally.
