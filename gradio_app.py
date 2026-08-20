"""
Gradio web app for the Voice Cloning & Lip-Sync pipeline.

This is the "flexible website" version: upload a video (and optionally a
separate voice reference clip), pick a target language, click Run — get
a downloadable dubbed video back. Works locally (`python gradio_app.py`)
and deploys as-is to Hugging Face Spaces for a real public URL.
"""

import os
import tempfile
import traceback

import gradio as gr

from src.pipeline import DubbingPipeline
from src.utils import load_config

CONFIG_PATH = os.environ.get("PIPELINE_CONFIG", "config/config.yaml")

LANGUAGES = {
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Mandarin Chinese": "zh-cn",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Russian": "ru",
    "Korean": "ko",
    "Italian": "it",
    "Turkish": "tr",
}


def run_pipeline(input_video, voice_reference, target_language_label, progress=gr.Progress()):
    """Callback wired to the Gradio Run button."""
    if input_video is None:
        raise gr.Error("Upload a source video first.")

    target_lang = LANGUAGES.get(target_language_label, "hi")

    try:
        progress(0.05, desc="Loading configuration...")
        config = load_config(CONFIG_PATH)
        pipeline = DubbingPipeline(config)

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "dubbed_output.mp4")

            progress(0.15, desc="Analyzing video & extracting audio...")
            result_path = pipeline.run(
                input_video=input_video,
                output_video=output_path,
                target_lang=target_lang,
                speaker_reference_audio=voice_reference,
            )

            # Gradio needs the file to persist after the temp dir closes —
            # copy it to a stable location before the context manager exits.
            persistent_path = os.path.join(
                tempfile.gettempdir(), f"dubbed_{os.path.basename(result_path)}"
            )
            with open(result_path, "rb") as src, open(persistent_path, "wb") as dst:
                dst.write(src.read())

            progress(1.0, desc="Done!")
            return persistent_path, "✅ Dubbing complete."

    except Exception as e:
        traceback.print_exc()
        raise gr.Error(f"Pipeline failed: {e}")


with gr.Blocks(title="Voice Cloning & Lip-Sync Studio") as demo:
    gr.Markdown(
        """
        # 🎙️ Voice Cloning & Lip-Sync Studio
        Upload a video, choose a target language, and get back a naturally
        dubbed version in the speaker's own cloned voice, with lips synced
        to the new audio.

        **Ethical use:** only clone voices with explicit consent. Disclose
        synthetic/dubbed media where required.
        """
    )

    with gr.Row():
        with gr.Column():
            input_video = gr.Video(label="Source video", sources=["upload"])
            voice_reference = gr.Audio(
                label="Optional: separate voice reference clip (defaults to the video's own audio)",
                sources=["upload"],
                type="filepath",
            )
            target_language_label = gr.Dropdown(
                choices=list(LANGUAGES.keys()),
                value="Hindi",
                label="Target language",
            )
            run_btn = gr.Button("🚀 Run dubbing pipeline", variant="primary")

        with gr.Column():
            output_video = gr.Video(label="Dubbed output")
            status = gr.Textbox(label="Status", interactive=False)

    run_btn.click(
        fn=run_pipeline,
        inputs=[input_video, voice_reference, target_language_label],
        outputs=[output_video, status],
    )

    gr.Markdown(
        """
        ---
        ⚠️ First run downloads several GB of model weights (Whisper, NLLB,
        XTTS-v2) and Wav2Lip checkpoints must be placed in `weights/`
        beforehand — see the repo README. A GPU is strongly recommended;
        on CPU this can take several minutes per short clip.
        """
    )


if __name__ == "__main__":
    demo.queue().launch()
