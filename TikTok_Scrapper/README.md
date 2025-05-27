# TikTok Scraper

A simple Python tool to extract information and download videos from TikTok URLs.

## Features

- Extract video metadata (likes, views, comments, author, etc.)
- Download TikTok videos
- Save metadata to JSON files

## Requirements

- Python 3.10+
- Required packages: requests (external), json, os, re, time, urllib.parse (standard library)


## Usage

You can run the script directly:

```sh
$ python main.py <URL>
```

## Project Structure

```sh
.
├── main.py                # Main script with implementation
├── README.md              # This file
└── tiktok/                # Directory for downloaded videos and metadata
    ├── tiktok_12345.json  # Example JSON metadata file
    └── tiktok_12345.mp4   # Example downloaded video file
```

## Demo

```sh
$ python3 main.py  https://www.tiktok.com/@meomeo_nhwuynk/video/7505474931090541831
Video URL: https://www.tiktok.com/@meomeo_nhwuynk/video/7505474931090541831

Extracting video information...

Video ID: 7505474931090541831
Author: Nó tên Cám
Date: 2025-05-18 00:56:07
Views: 126900
Likes: 7460
Comments: 96
Hashtags:

Downloading video...

Trying web embed URL: https://www.tiktok.com/embed/v2/7505474931090541831
Video saved to: /mnt/e/LENOVO/Documents/miniProject/TikTok_Scrapper/tiktok/tiktok_7505474931090541831.mp4

$ ls tiktok
tiktok_7505474931090541831.json  tiktok_7505474931090541831.mp4
```
