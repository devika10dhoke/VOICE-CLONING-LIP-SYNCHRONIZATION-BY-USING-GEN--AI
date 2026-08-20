"""
Streamlit demo UI for the Voice Cloning & Lip Synchronization pipeline.

Run with:
    streamlit run app.py
"""

import os
import tempfile

import streamlit as st

from src.pipeline import DubbingPipeline
from src.utils import load_config

st.set_page_config(page_title="Voice Cloning & Lip-Sync Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Voice Cloning & Lip-Sync Studio")
st.caption(
    "Upload a video, choose a target language, and generate a naturally "
    "dubbed, lip-synced version in the speaker's own cloned voice."
)

with st.sidebar:
    st.header("⚙️ Settings")
    config_path = st.text_input("Config file", value="config/config.yaml")
    target_lang = st.text_input("Target language code (e.g. hi, fr, es)", value="hi")
    st.markdown("---")
    st.markdown(
        "**Ethical use notice:** Only clone voices with explicit consent. "
        "Disclose synthetic/dubbed media where required."
    )

uploaded_video = st.file_uploader("Upload source video", type=["mp4", "mov", "avi"])
uploaded_speaker_ref = st.file_uploader(
    "Optional: separate voice reference clip (defaults to the video's own audio)",
    type=["wav", "mp3"],
)

if st.button("🚀 Run dubbing pipeline", disabled=uploaded_video is None):
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = os.path.join(tmp_dir, "input.mp4")
        with open(input_path, "wb") as f:
            f.write(uploaded_video.read())

        speaker_ref_path = None
        if uploaded_speaker_ref:
            speaker_ref_path = os.path.join(tmp_dir, "voice_ref.wav")
            with open(speaker_ref_path, "wb") as f:
                f.write(uploaded_speaker_ref.read())

        output_path = os.path.join(tmp_dir, "output.mp4")

        with st.spinner("Running pipeline — this can take a while on CPU..."):
            try:
                config = load_config(config_path)
                pipeline = DubbingPipeline(config)
                pipeline.run(
                    input_video=input_path,
                    output_video=output_path,
                    target_lang=target_lang,
                    speaker_reference_audio=speaker_ref_path,
                )
                st.success("Done!")
                st.video(output_path)
                with open(output_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download dubbed video", f, file_name="dubbed_output.mp4"
                    )
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
