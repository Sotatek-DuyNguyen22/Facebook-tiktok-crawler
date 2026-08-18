#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from urllib.parse import quote_plus

import yt_dlp


TIKTOK_VIDEO_PATTERN = re.compile(
    r'(?:https?://(?:www\.)?tiktok\.com)?/@([A-Za-z0-9._-]+)/video/(\d{8,})'
)


def common_options(cookies: Path | None) -> dict:
    options = {
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
    }
    if cookies:
        options["cookiefile"] = str(cookies)
    return options


def search_tiktok(keyword: str, cookies: Path | None) -> list[str]:
    search_url = "https://www.tiktok.com/search/video?q=" + quote_plus(keyword)
    options = common_options(cookies)
    options["quiet"] = True

    with yt_dlp.YoutubeDL(options) as ydl:
        response = ydl.urlopen(search_url)
        html = response.read().decode("utf-8", "replace")

    html = html.replace(r"\/", "/").replace(r"\u002F", "/")
    return [
        f"https://www.tiktok.com/@{username}/video/{video_id}"
        for username, video_id in TIKTOK_VIDEO_PATTERN.findall(html)
    ]


def download_audio(
    urls: list[str], output_dir: Path, cookies: Path | None
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    options = common_options(cookies)
    options.update(
        {
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
    )

    with yt_dlp.YoutubeDL(options) as ydl:
        for url in urls:
            print(f"Downloading: {url}")
            try:
                ydl.download([url])
            except Exception as error:
                print(f"Failed: {url} | {error}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search TikTok by keyword and download audio."
    )
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cookies", type=Path)
    parser.add_argument("--max-results", type=int, default=5)
    args = parser.parse_args()

    urls = search_tiktok(args.keyword, args.cookies)[: args.max_results]
    print(f"Found {len(urls)} raw result(s)")
    if not urls:
        print("No video URLs found. TikTok may require cookies or rendering.")
        return
    download_audio(urls, args.out, args.cookies)


if __name__ == "__main__":
    main()
