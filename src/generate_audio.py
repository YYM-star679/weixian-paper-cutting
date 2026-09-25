#!/usr/bin/env python3
"""用 edge-tts 为每一段旁白生成音频（assets/audio/seg_XX.mp3）。"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-4%"


def main():
    segs = json.load(open(os.path.join(ROOT, "src", "segments.json"), encoding="utf-8"))
    out_dir = os.path.join(ROOT, "assets", "audio")
    os.makedirs(out_dir, exist_ok=True)

    for seg in segs:
        i = seg["id"]
        out = os.path.join(out_dir, f"seg_{i:02d}.mp3")
        print(f"[{i}/{len(segs)}] 生成旁白音频 -> {os.path.basename(out)}")
        subprocess.run(
            [
                sys.executable, "-m", "edge_tts",
                "--voice", VOICE,
                "--rate", RATE,
                "--text", seg["narration"],
                "--write-media", out,
            ],
            check=True,
        )
    print("全部音频生成完成。")


if __name__ == "__main__":
    main()
