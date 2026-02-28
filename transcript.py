import re
import subprocess
import json
import os


def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_url):
    video_id = extract_video_id(video_url)

    if not video_id:
        return None, "Invalid YouTube URL."

    try:
        command = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "json3",
            "--output", "%(id)s",
            video_url
        ]

        subprocess.run(command, check=True)

        subtitle_file = f"{video_id}.en.json3"

        if not os.path.exists(subtitle_file):
            return None, "Transcript not available."

        with open(subtitle_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        transcript = ""

        for event in data.get("events", []):
            if "segs" in event:
                for seg in event["segs"]:
                    transcript += seg.get("utf8", "")

        os.remove(subtitle_file)

        if transcript.strip() == "":
            return None, "Transcript is empty."

        return transcript, None

    except Exception:
        return None, "Transcript not available."