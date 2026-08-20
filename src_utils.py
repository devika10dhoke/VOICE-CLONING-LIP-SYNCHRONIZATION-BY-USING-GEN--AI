"""Shared helper functions: config loading, logging, ffmpeg wrappers, I/O."""

import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """Load the pipeline YAML configuration file."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_logger(name: str, config: Dict[str, Any] = None) -> logging.Logger:
    """Create a configured logger. Falls back to INFO/console-only if no config given."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    level_name = "INFO"
    log_file = None
    if config and "logging" in config:
        level_name = config["logging"].get("level", "INFO")
        log_file = config["logging"].get("log_file")

    logger.setLevel(getattr(logging, level_name, logging.INFO))
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def ensure_dir(path: str) -> Path:
    """Create directory if it doesn't exist and return it as a Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def run_ffmpeg(cmd: list, logger: logging.Logger = None) -> None:
    """Run an ffmpeg command (list of args, NOT including 'ffmpeg' itself)."""
    full_cmd = ["ffmpeg", "-y", "-loglevel", "error"] + cmd
    if logger:
        logger.debug("Running: %s", " ".join(full_cmd))
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr}")


def extract_audio(video_path: str, output_wav: str, sample_rate: int = 16000) -> str:
    """Extract mono audio track from a video file as a WAV file."""
    run_ffmpeg(
        [
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", str(sample_rate),
            "-ac", "1",
            output_wav,
        ]
    )
    return output_wav


def mux_audio_video(video_path: str, audio_path: str, output_path: str) -> str:
    """Combine a (silent or replaced-audio) video with a new audio track."""
    run_ffmpeg(
        [
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path,
        ]
    )
    return output_path


def file_exists_or_raise(path: str, description: str = "file") -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{description} not found at: {path}")
