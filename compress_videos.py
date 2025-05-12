#!/usr/bin/env python3
import os
import subprocess
import argparse

def compress_video(input_path, output_path, crf=28, preset='medium'):
    """
    Uses ffmpeg to re-encode a video without altering resolution:
      - H.264 video codec with adjustable CRF (quality)
      - AAC audio @ 128 kbps
    """
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vcodec', 'libx264',
        '-crf', str(crf),
        '-preset', preset,
        '-acodec', 'aac',
        '-b:a', '128k',
        '-y',  # overwrite output if it exists
        output_path
    ]
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(
        description='Recursively compress all videos under a folder (keep original resolution)'
    )
    parser.add_argument(
        '--root_dir',
        help='Root directory to scan for videos'
    )
    parser.add_argument(
        '--output_dir',
        help=(
            'Base output directory (will mirror subfolder structure). '
            'If omitted, compressed files are placed alongside originals with "_compressed" suffix.'
        ),
        default=None
    )
    parser.add_argument(
        '--crf',
        type=int,
        default=20,
        help='CRF (quality) for H.264; lower = better quality/larger file'
    )
    parser.add_argument(
        '--preset',
        default='medium',
        choices=[
            'ultrafast','superfast','veryfast','faster','fast',
            'medium','slow','slower','veryslow'
        ],
        help='FFmpeg speed/quality preset'
    )
    args = parser.parse_args()

    # Video extensions to process
    video_exts = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')

    for dirpath, _, filenames in os.walk(args.root_dir):
        for fname in filenames:
            if fname.lower().endswith(video_exts):
                src = os.path.join(dirpath, fname)
                rel = os.path.relpath(dirpath, args.root_dir)
                name, ext = os.path.splitext(fname)

                if args.output_dir:
                    dst_dir = os.path.join(args.output_dir, rel)
                    os.makedirs(dst_dir, exist_ok=True)
                    dst = os.path.join(dst_dir, f"{name}{ext}")
                else:
                    dst = os.path.join(dirpath, f"{name}")

                print(f"Compressing:\n  {src}\n→\n  {dst}")
                try:
                    compress_video(
                        input_path=src,
                        output_path=dst,
                        crf=args.crf,
                        preset=args.preset
                    )
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  Failed to compress {src}: {e}")

if __name__ == "__main__":
    main()
