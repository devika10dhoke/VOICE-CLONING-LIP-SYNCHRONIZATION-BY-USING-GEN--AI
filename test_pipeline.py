"""
Basic smoke tests for the pipeline modules.

These tests focus on config loading, utility functions, and object
construction — not full model inference (which requires GPU/weights
and is out of scope for CI). Extend with integration tests once
model weights are available in your environment.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import load_config, ensure_dir  # noqa: E402
from src.video_analysis import VideoAnalyzer  # noqa: E402
from src.transcription import Transcriber  # noqa: E402
from src.translation import Translator  # noqa: E402
from src.voice_cloning import VoiceCloner  # noqa: E402
from src.lip_sync import LipSyncer  # noqa: E402


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")


@pytest.fixture(scope="module")
def config():
    return load_config(CONFIG_PATH)


def test_config_loads(config):
    assert "video_analysis" in config
    assert "transcription" in config
    assert "translation" in config
    assert "voice_cloning" in config
    assert "lip_sync" in config


def test_ensure_dir(tmp_path):
    target = tmp_path / "nested" / "dir"
    result = ensure_dir(str(target))
    assert result.exists()
    assert result.is_dir()


def test_video_analyzer_constructs(config):
    analyzer = VideoAnalyzer(config)
    assert analyzer.config == config


def test_transcriber_constructs(config):
    transcriber = Transcriber(config)
    assert transcriber.config == config


def test_translator_constructs(config):
    translator = Translator(config)
    assert translator.config == config


def test_voice_cloner_constructs(config):
    cloner = VoiceCloner(config)
    assert cloner.config == config


def test_lip_syncer_constructs(config):
    syncer = LipSyncer(config)
    assert syncer.config == config


def test_lip_sync_raises_on_missing_files(config, tmp_path):
    syncer = LipSyncer(config)
    with pytest.raises(FileNotFoundError):
        syncer.run_inference(
            face_video_path=str(tmp_path / "nope.mp4"),
            audio_path=str(tmp_path / "nope.wav"),
            output_path=str(tmp_path / "out.mp4"),
        )
