"""
Transcription
=============
Speech-to-text using OpenAI Whisper. Produces both the full transcript
and word/segment-level timestamps, which downstream translation and
voice-cloning stages use to preserve timing.
"""

import argparse
import json
from typing import Any, Dict

from src.utils import get_logger, load_config


class Transcriber:
    """Wraps a Whisper model for source-language speech-to-text."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model

        import whisper

        model_size = self.config.get("transcription", {}).get("model_size", "medium")
        device = self.config.get("device", "cpu")
        self.logger.info("Loading Whisper model '%s' on %s", model_size, device)
        self._model = whisper.load_model(model_size, device=device)
        return self._model

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe an audio file. Returns Whisper's segment/word-level result dict."""
        model = self._load_model()
        cfg = self.config.get("transcription", {})
        language = cfg.get("language", "auto")

        options = {"task": cfg.get("task", "transcribe"), "word_timestamps": True}
        if language and language != "auto":
            options["language"] = language

        self.logger.info("Transcribing %s", audio_path)
        result = model.transcribe(audio_path, **options)

        segments = [
            {
                "id": seg["id"],
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            }
            for seg in result.get("segments", [])
        ]

        return {
            "language": result.get("language"),
            "text": result.get("text", "").strip(),
            "segments": segments,
        }

    def transcribe_and_save(self, audio_path: str, output_json: str) -> Dict[str, Any]:
        result = self.transcribe(audio_path)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        self.logger.info("Transcript saved to %s", output_json)
        return result


def main():
    parser = argparse.ArgumentParser(description="Transcribe an audio/video file.")
    parser.add_argument("--input", required=True, help="Path to audio or video file")
    parser.add_argument("--output", default="temp/transcript.json")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    transcriber = Transcriber(config)
    result = transcriber.transcribe_and_save(args.input, args.output)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
