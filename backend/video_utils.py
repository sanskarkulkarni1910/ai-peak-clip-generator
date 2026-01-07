import subprocess

def crop_vertical(input_file, output_file, start, duration):
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-t", str(duration),
        "-i", input_file,
        "-vf", "crop=ih*9/16:ih,scale=720:1280",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-c:a", "aac",
        output_file
    ]
    subprocess.run(cmd, check=True)

def burn_caption(video_in, video_out, caption_text):
    import subprocess

    # safety: empty caption skip
    if not caption_text:
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_in, "-c", "copy", video_out]
        )
        return

    drawtext = (
        "drawtext="
        "fontfile=C\\:/Windows/Fonts/arial.ttf:"
        "text='{}':"
        "fontcolor=white:"
        "fontsize=42:"
        "box=1:"
        "boxcolor=black@0.7:"
        "boxborderw=12:"
        "x=(w-text_w)/2:"
        "y=h-(text_h*2)"
    ).format(caption_text.replace("'", ""))

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", video_in,
            "-vf", drawtext,
            "-c:a", "copy",
            video_out
        ]
    )


