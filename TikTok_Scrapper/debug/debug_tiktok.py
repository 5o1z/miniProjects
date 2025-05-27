#!/usr/bin/env python3

import requests
import re
import json
import sys

def debug_tiktok_page(url):
    print(f"Debugging TikTok URL: {url}")

    # Setup headers
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "TE": "trailers"
    }

    # Handle URL redirects if it's a short URL
    if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
        try:
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                url = response.url
                print(f"Resolved to: {url}")
            else:
                print(f"Failed to resolve shortened URL: {response.status_code}")
                return
        except requests.RequestException as e:
            print(f"Error resolving shortened URL: {str(e)}")
            return

    # Make request to the actual page
    try:
        print("Fetching page...")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"Failed to fetch video page: HTTP {response.status_code}")
            return

        html_content = response.text

        # Save HTML content for inspection
        with open("tiktok_debug_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved full HTML content to tiktok_debug_page.html")

        # Try different JSON data patterns
        json_patterns = [
            # Original pattern
            r'<script id="SIGI_STATE" type="application/json">(.*?)</script>',

            r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>',
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            r'window\[\'SIGI_STATE\'\]=(.*?);</script>',
            r'<script>window\.__INIT_PROPS__\s*=\s*(\{.*?\})</script>',
        ]

        for i, pattern in enumerate(json_patterns):
            print(f"\nTrying pattern {i+1}: {pattern}")
            matches = re.findall(pattern, html_content, re.DOTALL)

            if matches:
                print(f"Found {len(matches)} match(es)!")

                for j, match in enumerate(matches):
                    print(f"\nMatch {j+1} (first 200 chars):")
                    print(match[:200] + "...")

                    try:
                        json_obj = json.loads(match)
                        print("Valid JSON!")

                        output_file = f"tiktok_debug_pattern{i+1}_match{j+1}.json"
                        with open(output_file, "w", encoding="utf-8") as f:
                            json.dump(json_obj, f, ensure_ascii=False, indent=2)
                        print(f"Saved JSON data to {output_file}")

                        if 'ItemModule' in json_obj:
                            print("Found ItemModule in JSON!")
                        if 'ItemList' in json_obj:
                            print("Found ItemList in JSON!")
                        if 'props' in json_obj and 'pageProps' in json_obj['props']:
                            print("Found props.pageProps in JSON!")
                    except json.JSONDecodeError:
                        print("Not valid JSON")
            else:
                print("No matches")

    except Exception as e:
        print(f"Error during debugging: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter TikTok URL to debug: ")

    debug_tiktok_page(url)
