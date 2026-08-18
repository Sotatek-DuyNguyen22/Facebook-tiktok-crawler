#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from urllib.parse import quote_plus

import yt_dlp


VIDEO_PATTERNS = [
    (re.compile(r'/videos/(?:[^/?#]+/)?(\d{8,})'), "video"),
    (re.compile(r'"video_id"\s*:\s*"(\d{8,})"'), "video"),
    (re.compile(r'"videoId"\s*:\s*"(\d{8,})"'), "video"),
    (re.compile(r'/reel/(\d{8,})'), "reel"),
]


def search_facebook(keyword: str, cookies: Path | None) -> list[str]:
    search_url = (
        "https://www.facebook.com/search/videos/?q=" + quote_plus(keyword)
    )
    options = {
        "quiet": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
            )
        },
    }
    if cookies:
        options["cookiefile"] = str(cookies)

    with yt_dlp.YoutubeDL(options) as ydl:
        response = ydl.urlopen(search_url)
        html = response.read().decode("utf-8", "replace")

    html = html.replace(r"\/", "/")
    urls: list[str] = []
    for pattern, kind in VIDEO_PATTERNS:
        for video_id in pattern.findall(html):
            if kind == "reel":
                urls.append(f"https://www.facebook.com/reel/{video_id}")
            else:
                urls.append(f"https://www.facebook.com/watch/?v={video_id}")
    return urls


def download_audio(
    urls: list[str], output_dir: Path, cookies: Path | None
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(id)s - %(title).100B.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "wav"}
        ],
        "postprocessor_args": {
            "extractaudio": ["-ar", "16000", "-ac", "1"]
        },
    }
    if cookies:
        options["cookiefile"] = str(cookies)

    with yt_dlp.YoutubeDL(options) as ydl:
        for url in urls:
            print(f"Downloading: {url}")
            try:
                ydl.download([url])
            except Exception as error:
                print(f"Failed: {url} | {error}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search Facebook by keyword and download audio."
    )
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cookies", type=Path)
    parser.add_argument("--max-results", type=int, default=5)
    args = parser.parse_args()

    urls = search_facebook(args.keyword, args.cookies)[: args.max_results]
    print(f"Found {len(urls)} raw result(s)")
    download_audio(urls, args.out, args.cookies)


if __name__ == "__main__":
    main()
