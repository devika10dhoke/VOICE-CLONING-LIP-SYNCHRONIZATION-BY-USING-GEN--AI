"""
Lip Synchronization
===================
Wraps Wav2Lip (GAN-based visual dubbing model) to regenerate the mouth
region of the source video so it matches the newly synthesized, cloned
audio track.

NOTE: This module expects the Wav2Lip repository's inference code to be
importable (e.g. installed as a package or vendored under `third_party/wav2lip`)
and a pretrained checkpoint (`wav2lip_gan.pth`) downloaded per the README.
The `run_inference` method shells out to Wav2Lip's `inference.py` for
maximum compatibility with upstream updates; swap for a direct Python
import if you vendor the repo.
"""

import argparse
import os
import subprocess
from typing import Optional

from src.utils import ensure_dir, file_exists_or_raise, get_logger, load_config


class LipSyncer:
    """Wraps Wav2Lip to generate a lip-synced output video."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)

    def run_inference(
        self,
        face_video_path: str,
        audio_path: str,
        output_path: str,
        wav2lip_repo_path: str = "third_party/Wav2Lip",
    ) -> str:
        """
        Run Wav2Lip inference: replaces the mouth region of `face_video_path`
        with lip movement matching `audio_path`.

        Requires the Wav2Lip repo cloned at `wav2lip_repo_path` with its own
        Python environment/deps (see Wav2Lip's own requirements.txt) and the
        checkpoint referenced in config -> lip_sync.checkpoint_path.
        """
        cfg = self.config.get("lip_sync", {})
        checkpoint_path = cfg.get("checkpoint_path", "weights/wav2lip_gan.pth")

        file_exists_or_raise(face_video_path, "input video")
        file_exists_or_raise(audio_path, "audio track")
        file_exists_or_raise(checkpoint_path, "Wav2Lip checkpoint")

        inference_script = os.path.join(wav2lip_repo_path, "inference.py")
        file_exists_or_raise(inference_script, "Wav2Lip inference.py")

        ensure_dir(os.path.dirname(output_path) or ".")

        cmd = [
            "python", inference_script,
            "--checkpoint_path", checkpoint_path,
            "--face", face_video_path,
            "--audio", audio_path,
            "--outfile", output_path,
            "--resize_factor", str(cfg.get("resize_factor", 1)),
            "--face_det_batch_size", str(cfg.get("face_det_batch_size", 16)),
            "--wav2lip_batch_size", str(cfg.get("wav2lip_batch_size", 128)),
        ]
        pads = cfg.get("pads")
        if pads:
            cmd += ["--pads"] + [str(p) for p in pads]
        if cfg.get("nosmooth"):
            cmd.append("--nosmooth")

        self.logger.info("Running Wav2Lip: %s", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Wav2Lip inference failed:\n{result.stderr}")

        self.logger.info("Lip-synced video written to %s", output_path)
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Run lip-sync inference (Wav2Lip).")
    parser.add_argument("--video", required=True, help="Source face video")
    parser.add_argument("--audio", required=True, help="Target audio track")
    parser.add_argument("--output", default="temp/lip_synced_output.mp4")
    parser.add_argument("--wav2lip-repo", default="third_party/Wav2Lip")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    syncer = LipSyncer(config)
    out_path = syncer.run_inference(
        args.video, args.audio, args.output, wav2lip_repo_path=args.wav2lip_repo
    )
    print(f"Output: {out_path}")


if __name__ == "__main__":
    main()
