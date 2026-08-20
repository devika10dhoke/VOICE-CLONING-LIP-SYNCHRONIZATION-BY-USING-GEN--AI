"""
End-to-End Pipeline
====================
Orchestrates: Video Analysis -> Transcription -> Translation ->
Voice Cloning -> Lip Sync -> final dubbed output video.
"""

import argparse
import json
import os

from src.lip_sync import LipSyncer
from src.transcription import Transcriber
from src.translation import Translator
from src.utils import ensure_dir, get_logger, load_config
from src.video_analysis import VideoAnalyzer
from src.voice_cloning import VoiceCloner


class DubbingPipeline:
    """Runs the full video-analysis -> translation -> voice-clone -> lip-sync flow."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)

        self.video_analyzer = VideoAnalyzer(config)
        self.transcriber = Transcriber(config)
        self.translator = Translator(config)
        self.voice_cloner = VoiceCloner(config)
        self.lip_syncer = LipSyncer(config)

    def run(
        self,
        input_video: str,
        output_video: str,
        target_lang: str = None,
        speaker_reference_audio: str = None,
    ) -> str:
        paths = self.config.get("paths", {})
        temp_dir = ensure_dir(paths.get("temp_dir", "temp"))
        ensure_dir(paths.get("output_dir", "outputs"))

        # 1. Video analysis: extract audio + frames
        self.logger.info("=== Stage 1/5: Video analysis ===")
        analysis = self.video_analyzer.analyze(input_video, str(temp_dir / "analysis"))
        source_audio = analysis["metadata"]["audio_path"]

        # 2. Transcription
        self.logger.info("=== Stage 2/5: Transcription ===")
        transcript_path = str(temp_dir / "transcript.json")
        transcript = self.transcriber.transcribe_and_save(source_audio, transcript_path)

        # 3. Translation
        self.logger.info("=== Stage 3/5: Translation ===")
        translated_path = str(temp_dir / "translated_transcript.json")
        translated = self.translator.translate_transcript_file(
            transcript_path, translated_path, target_lang=target_lang
        )
        full_translated_text = " ".join(
            seg["translated_text"] for seg in translated["segments"]
        )

        # 4. Voice cloning
        self.logger.info("=== Stage 4/5: Voice cloning ===")
        speaker_ref = speaker_reference_audio or self.config.get(
            "voice_cloning", {}
        ).get("speaker_reference_audio", source_audio)
        cloned_audio_path = str(temp_dir / "cloned_voice.wav")
        self.voice_cloner.clone_and_synthesize(
            text=full_translated_text,
            speaker_reference_audio=speaker_ref,
            output_path=cloned_audio_path,
            target_language=target_lang,
        )

        # 5. Lip sync
        self.logger.info("=== Stage 5/5: Lip synchronization ===")
        ensure_dir(os.path.dirname(output_video) or ".")
        self.lip_syncer.run_inference(
            face_video_path=input_video,
            audio_path=cloned_audio_path,
            output_path=output_video,
        )

        self.logger.info("Pipeline complete. Output: %s", output_video)
        return output_video


def main():
    parser = argparse.ArgumentParser(
        description="Run the full voice-cloning + lip-sync dubbing pipeline."
    )
    parser.add_argument("--input", required=True, help="Path to input video")
    parser.add_argument("--output", required=True, help="Path to output video")
    parser.add_argument("--target-lang", default=None, help="Target language code")
    parser.add_argument(
        "--speaker-audio",
        default=None,
        help="Reference audio for the voice to clone (defaults to source audio)",
    )
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    pipeline = DubbingPipeline(config)
    output_path = pipeline.run(
        input_video=args.input,
        output_video=args.output,
        target_lang=args.target_lang,
        speaker_reference_audio=args.speaker_audio,
    )
    print(json.dumps({"output_video": output_path}, indent=2))


if __name__ == "__main__":
    main()
