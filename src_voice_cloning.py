"""
Voice Cloning
=============
Few-shot speaker-conditioned text-to-speech using Coqui TTS (XTTS-v2).
Given a short reference clip of the target speaker's voice and translated
text, synthesizes speech in the target language that preserves the
speaker's vocal identity.
"""

import argparse
import json
import os
from typing import Any, Dict, List

from src.utils import ensure_dir, file_exists_or_raise, get_logger, load_config


class VoiceCloner:
    """Wraps Coqui XTTS-v2 for speaker-conditioned multilingual TTS."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)
        self._tts = None

    def _load_model(self):
        if self._tts is not None:
            return self._tts

        from TTS.api import TTS

        cfg = self.config.get("voice_cloning", {})
        model_name = cfg.get(
            "model_name", "tts_models/multilingual/multi-dataset/xtts_v2"
        )
        device = self.config.get("device", "cpu")

        self.logger.info("Loading TTS model '%s' on %s", model_name, device)
        self._tts = TTS(model_name).to(device)
        return self._tts

    def clone_and_synthesize(
        self,
        text: str,
        speaker_reference_audio: str,
        output_path: str,
        target_language: str = None,
    ) -> str:
        """Synthesize `text` in the cloned voice of the speaker reference clip."""
        file_exists_or_raise(speaker_reference_audio, "speaker reference audio")
        cfg = self.config.get("voice_cloning", {})
        target_language = target_language or cfg.get("target_language", "en")

        tts = self._load_model()
        ensure_dir(os.path.dirname(output_path) or ".")

        self.logger.info(
            "Synthesizing (%d chars, lang=%s) -> %s",
            len(text),
            target_language,
            output_path,
        )
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_reference_audio,
            language=target_language,
            file_path=output_path,
        )
        return output_path

    def synthesize_segments(
        self,
        segments: List[Dict[str, Any]],
        speaker_reference_audio: str,
        output_dir: str,
        target_language: str = None,
        text_key: str = "translated_text",
    ) -> List[Dict[str, Any]]:
        """Synthesize each translated transcript segment to its own audio clip."""
        ensure_dir(output_dir)
        results = []
        for seg in segments:
            out_path = os.path.join(output_dir, f"segment_{seg['id']:04d}.wav")
            self.clone_and_synthesize(
                text=seg[text_key],
                speaker_reference_audio=speaker_reference_audio,
                output_path=out_path,
                target_language=target_language,
            )
            results.append({**seg, "audio_path": out_path})
        return results


def main():
    parser = argparse.ArgumentParser(description="Clone a voice and synthesize speech.")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    parser.add_argument(
        "--speaker-audio", required=True, help="Reference audio of the target voice"
    )
    parser.add_argument("--output", default="temp/cloned_voice.wav")
    parser.add_argument("--target-lang", default=None)
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    cloner = VoiceCloner(config)
    out_path = cloner.clone_and_synthesize(
        text=args.text,
        speaker_reference_audio=args.speaker_audio,
        output_path=args.output,
        target_language=args.target_lang,
    )
    print(json.dumps({"output_audio": out_path}, indent=2))


if __name__ == "__main__":
    main()
