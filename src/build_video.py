#!/usr/bin/env python3
"""把幻灯片 PNG 与旁白音频合成为视频，并拼接成最终 MP4（video/weixian-paper-cutting.mp4）。"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = r"C:\Users\renai\Desktop\新建文件夹\tools\ffmpeg-9.0.2-essentials_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\renai\Desktop\新建文件夹\tools\ffmpeg-9.0.2-essentials_build\bin\ffprobe.exe"

FPS = 25
PAD_LEAD = 0.25
PAD_TAIL = 0.35
FADE = 0.25
BG_COLOR = "0xFBF6EE"


def probe(path):
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def main():
    segs = json.load(open(os.path.join(ROOT, "src", "segments.json"), encoding="utf-8"))
    n = len(segs)
    build = os.path.join(ROOT, "build")
    os.makedirs(build, exist_ok=True)

    for seg in segs:
        i = seg["id"]
        audio = os.path.join(ROOT, "assets", "audio", f"seg_{i:02d}.mp3")
        slide = os.path.join(ROOT, "assets", "slides", f"slide_{i:02d}.png")
        dur = probe(audio)
        D = dur + PAD_LEAD + PAD_TAIL
        out = os.path.join(build, f"seg_{i:02d}.mp4")

        af = (
            "[1:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"adelay={int(PAD_LEAD * 1000)}:all=1,apad,atrim=0:{D:.3f}[a]"
        )
        vf = (
            f"[0:v]scale=1920:1080,setsar=1,fps={FPS},format=yuv420p,"
            f"fade=t=in:st=0:d={FADE}:color={BG_COLOR},"
            f"fade=t=out:st={D - FADE:.3f}:d={FADE}:color={BG_COLOR}[v]"
        )
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-framerate", str(FPS), "-t", f"{D:.3f}", "-i", slide,
            "-i", audio,
            "-filter_complex", af + ";" + vf,
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
            "-shortest", out,
        ]
        print(f"[{i}/{n}] 合成片段：旁白 {dur:.2f}s -> 画面 {D:.2f}s")
        subprocess.run(cmd, check=True)

    with open(os.path.join(build, "concat.txt"), "w", encoding="utf-8") as f:
        for i in range(1, n + 1):
            f.write(f"file 'seg_{i:02d}.mp4'\n")

    final = os.path.join(ROOT, "video", "weixian-paper-cutting.mp4")
    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", "concat.txt", "-c", "copy", final,
    ]
    print("拼接全部片段…")
    subprocess.run(cmd, check=True, cwd=build)

    print("完成：", final)
    print("时长：%.2f 秒" % probe(final))


if __name__ == "__main__":
    main()
