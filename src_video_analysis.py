"""
Video Analysis
==============
Handles ingestion of the source video: extracting frames, isolating the
audio track, detecting/cropping faces, and producing basic scene metadata
that downstream stages (transcription, lip-sync) depend on.
"""

import argparse
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional

import cv2

from src.utils import ensure_dir, extract_audio, get_logger, load_config


@dataclass
class VideoMetadata:
    path: str
    fps: float
    frame_count: int
    width: int
    height: int
    duration_sec: float
    audio_path: Optional[str] = None


class VideoAnalyzer:
    """Extracts frames, audio, and face regions from an input video."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger(self.__class__.__name__, config)
        self._face_detector = None  # lazily initialized

    # ------------------------------------------------------------------ #
    # Metadata
    # ------------------------------------------------------------------ #
    def get_metadata(self, video_path: str) -> VideoMetadata:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        duration = frame_count / fps if fps else 0.0
        return VideoMetadata(
            path=video_path,
            fps=fps,
            frame_count=frame_count,
            width=width,
            height=height,
            duration_sec=duration,
        )

    # ------------------------------------------------------------------ #
    # Audio extraction
    # ------------------------------------------------------------------ #
    def extract_audio_track(self, video_path: str, output_dir: str) -> str:
        ensure_dir(output_dir)
        sample_rate = self.config.get("video_analysis", {}).get(
            "audio_sample_rate", 16000
        )
        out_wav = os.path.join(output_dir, "source_audio.wav")
        self.logger.info("Extracting audio track -> %s", out_wav)
        extract_audio(video_path, out_wav, sample_rate=sample_rate)
        return out_wav

    # ------------------------------------------------------------------ #
    # Frame sampling
    # ------------------------------------------------------------------ #
    def extract_frames(
        self, video_path: str, output_dir: str, sample_rate: Optional[int] = None
    ) -> List[str]:
        """Extract frames at the configured sample rate and save as JPEGs."""
        ensure_dir(output_dir)
        sample_rate = sample_rate or self.config.get("video_analysis", {}).get(
            "fps_sample_rate", 25
        )

        cap = cv2.VideoCapture(video_path)
        native_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        step = max(int(round(native_fps / sample_rate)), 1)

        frame_paths = []
        idx, saved = 0, 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % step == 0:
                out_path = os.path.join(output_dir, f"frame_{saved:06d}.jpg")
                cv2.imwrite(out_path, frame)
                frame_paths.append(out_path)
                saved += 1
            idx += 1
        cap.release()

        self.logger.info("Extracted %d frames to %s", saved, output_dir)
        return frame_paths

    # ------------------------------------------------------------------ #
    # Face detection
    # ------------------------------------------------------------------ #
    def _load_face_detector(self):
        if self._face_detector is not None:
            return self._face_detector

        backend = self.config.get("video_analysis", {}).get(
            "face_detector", "mediapipe"
        )
        if backend == "mediapipe":
            import mediapipe as mp

            self._face_detector = mp.solutions.face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5
            )
        else:
            import face_alignment

            self._face_detector = face_alignment.FaceAlignment(
                face_alignment.LandmarksType.TWO_D, flip_input=False
            )
        return self._face_detector

    def detect_face_bbox(self, frame_path: str) -> Optional[dict]:
        """Return a normalized bounding box {x, y, w, h} for the primary face, or None."""
        detector = self._load_face_detector()
        image = cv2.imread(frame_path)
        h, w = image.shape[:2]

        backend = self.config.get("video_analysis", {}).get(
            "face_detector", "mediapipe"
        )
        if backend == "mediapipe":
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = detector.process(rgb)
            if not results.detections:
                return None
            box = results.detections[0].location_data.relative_bounding_box
            return {
                "x": int(box.xmin * w),
                "y": int(box.ymin * h),
                "w": int(box.width * w),
                "h": int(box.height * h),
            }
        else:
            preds = detector.get_landmarks(image)
            if not preds:
                return None
            landmarks = preds[0]
            x_min, y_min = landmarks.min(axis=0)
            x_max, y_max = landmarks.max(axis=0)
            return {
                "x": int(x_min),
                "y": int(y_min),
                "w": int(x_max - x_min),
                "h": int(y_max - y_min),
            }

    # ------------------------------------------------------------------ #
    # Orchestration
    # ------------------------------------------------------------------ #
    def analyze(self, video_path: str, output_dir: str) -> dict:
        """Run full analysis: metadata + audio extraction + frame sampling."""
        ensure_dir(output_dir)
        metadata = self.get_metadata(video_path)
        metadata.audio_path = self.extract_audio_track(video_path, output_dir)
        frames_dir = os.path.join(output_dir, "frames")
        frame_paths = self.extract_frames(video_path, frames_dir)

        result = {
            "metadata": asdict(metadata),
            "num_frames_sampled": len(frame_paths),
            "frames_dir": frames_dir,
        }

        report_path = os.path.join(output_dir, "analysis_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        self.logger.info("Analysis report written to %s", report_path)
        return result


def main():
    parser = argparse.ArgumentParser(description="Analyze a source video.")
    parser.add_argument("--input", required=True, help="Path to input video")
    parser.add_argument(
        "--output-dir", default="temp/video_analysis", help="Output directory"
    )
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    analyzer = VideoAnalyzer(config)
    result = analyzer.analyze(args.input, args.output_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
