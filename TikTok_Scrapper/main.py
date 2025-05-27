import requests
import json
import os
import re
import time
import sys
import datetime
from urllib.parse import urlparse
from typing import Dict, Any, Tuple


class TikTokScraper:
    """
    A class for scraping TikTok videos and metadata.

    Attributes:
        headers (Dict[str, str]): HTTP headers for making requests
        user_agent (str): User agent string for HTTP requests
        output_dir (str): Directory for storing output files
        json_dir (str): Directory for storing JSON metadata
        video_dir (str): Directory for storing downloaded videos
    """

    def __init__(self):

        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        self.headers = {
            "User-Agent": self.user_agent,
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

        # Create directory structure if it doesn't exist
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok")
        self.json_dir = os.path.join(self.output_dir)
        self.video_dir = os.path.join(self.output_dir)

        for directory in [self.output_dir, self.json_dir, self.video_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)


    def normalize_url(self, url: str) -> str:
        """
        Convert short TikTok URLs to standard format.

        Args:
            url (str): TikTok URL (short or long format)

        Returns:
            str: Standardized TikTok URL
        """
        url = url.strip()

        # Check if it's already a standard URL
        if "tiktok.com/@" in url and "/video/" in url:
            return url

        # Handle shortened URLs (vm.tiktok.com)
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            try:
                response = requests.head(url, headers=self.headers, allow_redirects=True, timeout=10)
                # print(response)
                if response.status_code == 200:
                    return response.url
                else:
                    raise ValueError(f"Failed to resolve shortened URL: {response.status_code}")
            except requests.RequestException as e:
                raise ValueError(f"Error resolving shortened URL: {str(e)}")

        raise ValueError("Invalid TikTok URL format")


    def extract_video_id(self, url: str) -> str:
        """
        Extract the video ID from a TikTok URL.

        Args:
            url (str): TikTok standard URL

        Returns:
            str: Video ID
        """

        # Try to match the video ID pattern in the URL
        video_id_match = re.search(r'/video/(\d+)', url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Could not extract video ID from URL")


    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Scrape video information from a TikTok URL.

        Args:
            url (str): TikTok URL

        Returns:
            Dict[str, Any]: Dictionary containing video metadata
        """
        try:
            # Normalize the URL
            standard_url = self.normalize_url(url)

            # Get the video ID
            video_id = self.extract_video_id(standard_url)
            # Make request to the video page
            response = requests.get(standard_url, headers=self.headers, timeout=15)

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch video page: HTTP {response.status_code}")

            # Extract JSON data from the page
            html_content = response.text

            json_data_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'

            json_data_match = None

            json_data_match = re.search(json_data_pattern, html_content, re.DOTALL)
            # print(json_data_match)

            if not json_data_match:
                raise ValueError("Could not find JSON data in the page")

            try:
                json_data = json.loads(json_data_match.group(1))
                # print(json_data)

                # Extract video information from JSON data
                item_info = None
                default_scope = json_data.get("__DEFAULT_SCOPE__", {})
                webapp_video = default_scope.get("webapp.video-detail", {})
                item_list = webapp_video.get("itemInfo", {})
                item_info = item_list.get("itemStruct", {})

                if not item_info:
                    raise ValueError("Could not find video information in JSON data")

                # Extract statistics
                stats = item_info.get("stats", {})

                # Extract author information - handle both string and object formats
                author_info = item_info.get("author", {})
                if isinstance(author_info, dict):
                    author_name = author_info.get("nickname", "")
                else:
                    author_name = str(author_info)

                # Extract hashtags from challenges array
                hashtags_from_challenges = [tag.get("title", "") for tag in item_info.get("challenges", [])]

                # Extract hashtags from description as fallback
                description = item_info.get("desc", "")
                hashtags_from_description = []
                if description and not hashtags_from_challenges:
                    # Find all words starting with # in the description
                    hashtags_from_description = re.findall(r'#(\w+)', description)

                hashtags = hashtags_from_challenges if hashtags_from_challenges else hashtags_from_description

                # Convert the Unix timestamp to YYYY-MM-DD HH:MM:SS format
                timestamp = item_info.get("createTime", 0)
                if isinstance(timestamp, str):
                    timestamp = int(timestamp)
                formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else ""

                # Create structured video information
                video_info = {
                    "id": video_id,
                    "author_name": author_name,
                    "views": stats.get("playCount", 0),
                    "likes": stats.get("diggCount", 0),
                    "comments": stats.get("commentCount", 0),
                    "saves": stats.get("collectCount", 0),
                    "date": formatted_date,
                    "description": description,
                    "hashtag": hashtags
                }

                # Save JSON data
                self._save_json(video_id, video_info)

                return video_info
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON data from the page")

        except requests.RequestException as e:
            raise ValueError(f"Request error: {str(e)}")


    def download_video(self, url: str) -> str:
        """
        Download the TikTok video.

        Args:
            url (str): TikTok URL

        Returns:
            str: Path to the downloaded video file
        """
        try:
            video_info = self.get_video_info(url)
            video_id = video_info["id"]

            output_filename = f"tiktok_{video_id}.mp4"
            video_path = os.path.join(self.video_dir, output_filename)

            try:
                embed_url = f"https://www.tiktok.com/embed/{video_id}"
                print(f"Trying web embed URL: {embed_url}")

                embed_response = requests.get(embed_url, headers=self.headers, timeout=15)
                if embed_response.status_code == 200:
                    embed_content = embed_response.text
                    # print(embed_content)
                    video_match = re.search(r'<video[^>]+src="([^"]+)"', embed_content)
                    if video_match:
                        embed_video_url = video_match.group(1).replace('&amp;', '&')
                        video_response = requests.get(embed_video_url, headers=self.headers, stream=True, timeout=30)

                        if video_response.status_code == 200:
                            with open(video_path, 'wb') as f:
                                for chunk in video_response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                            return video_path
            except Exception as e:
                print(f"Embed method failed: {str(e)}")

        except requests.RequestException as e:
            raise ValueError(f"Request error: {str(e)}")


    def _save_json(self, video_id: str, data: Dict[str, Any]) -> str:
        """
        Save video metadata to a JSON file.

        Args:
            video_id (str): TikTok video ID
            data (Dict[str, Any]): Video metadata

        Returns:
            str: Path to the JSON file
        """
        filename = f"tiktok_{video_id}.json"
        file_path = os.path.join(self.json_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return file_path


if __name__ == "__main__":
    try:
        scraper = TikTokScraper()
        if len(sys.argv) < 2:
            print("Usage: python3 main.py <URL>")
        else:
            url = sys.argv[1]
            print(f"Video URL: {url}")

            print("\nExtracting video information...\n")
            video_info = scraper.get_video_info(url)
            print(f"Video ID: {video_info['id']}")
            print(f"Author: {video_info['author_name']}")
            print(f"Date: {video_info['date']}")
            print(f"Views: {video_info['views']}")
            print(f"Likes: {video_info['likes']}")
            print(f"Comments: {video_info['comments']}")
            print(f"Description: {video_info['description']}")
            print(f"Hashtags: {', '.join(video_info['hashtag'])}")

            print("\nDownloading video...\n")
            video_path = scraper.download_video(url)
            print(f"Video saved to: {video_path}")

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
