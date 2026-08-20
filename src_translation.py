"""
Translation
===========
Multilingual neural machine translation (default: Meta's NLLB-200)
used to translate the transcribed source-language segments into the
target language before voice cloning.
"""

import argparse
import json
from typing import Any, Dict, List

from src.utils import get_logger, load_config


class Translator:
    """Wraps a HuggingFace translation model (default NLLB-200)."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)
        self._model = None
        self._tokenizer = None

    def _load_model(self):
        if self._model is not None:
            return self._model, self._tokenizer

        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        cfg = self.config.get("translation", {})
        model_name = cfg.get("model_name", "facebook/nllb-200-distilled-600M")
        device = self.config.get("device", "cpu")

        self.logger.info("Loading translation model '%s' on %s", model_name, device)
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        return self._model, self._tokenizer

    def translate_text(
        self, text: str, source_lang: str = None, target_lang: str = None
    ) -> str:
        """Translate a single string of text."""
        cfg = self.config.get("translation", {})
        source_lang = source_lang or cfg.get("source_lang", "eng_Latn")
        target_lang = target_lang or cfg.get("target_lang", "hin_Deva")
        max_length = cfg.get("max_length", 400)
        device = self.config.get("device", "cpu")

        model, tokenizer = self._load_model()
        tokenizer.src_lang = source_lang

        inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)
        forced_bos_token_id = tokenizer.convert_tokens_to_ids(target_lang)

        generated = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=max_length,
        )
        return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

    def translate_segments(
        self, segments: List[Dict[str, Any]], source_lang: str = None, target_lang: str = None
    ) -> List[Dict[str, Any]]:
        """Translate each transcript segment while preserving timestamps."""
        translated = []
        for seg in segments:
            translated_text = self.translate_text(
                seg["text"], source_lang=source_lang, target_lang=target_lang
            )
            translated.append({**seg, "translated_text": translated_text})
            self.logger.debug("'%s' -> '%s'", seg["text"], translated_text)
        return translated

    def translate_transcript_file(
        self, transcript_json: str, output_json: str, target_lang: str = None
    ) -> Dict[str, Any]:
        with open(transcript_json, "r", encoding="utf-8") as f:
            transcript = json.load(f)

        translated_segments = self.translate_segments(
            transcript["segments"], target_lang=target_lang
        )
        result = {**transcript, "segments": translated_segments}

        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        self.logger.info("Translated transcript saved to %s", output_json)
        return result


def main():
    parser = argparse.ArgumentParser(description="Translate text or a transcript file.")
    parser.add_argument("--text", help="Raw text to translate")
    parser.add_argument("--transcript", help="Path to a transcript JSON from transcription.py")
    parser.add_argument("--output", default="temp/translated_transcript.json")
    parser.add_argument("--target-lang", default=None, help="Target language code")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    translator = Translator(config)

    if args.text:
        print(translator.translate_text(args.text, target_lang=args.target_lang))
    elif args.transcript:
        result = translator.translate_transcript_file(
            args.transcript, args.output, target_lang=args.target_lang
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        parser.error("Provide either --text or --transcript")


if __name__ == "__main__":
    main()
