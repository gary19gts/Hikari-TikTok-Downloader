"""
YT-DLP Engine for TikTok downloads
High-quality, reliable downloader with extensive format support

Copyright (C) 2025 Gary19gts

This program is dual-licensed:
1. GNU Affero General Public License v3 (AGPLv3) for open source use
2. Proprietary license for commercial/closed source use

For open source use:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

For commercial licensing, contact Gary19gts.

Author: Gary19gts
"""

import yt_dlp
import os
from pathlib import Path
import threading

class YtDlpEngine:
    def __init__(self):
        self.name = "yt-dlp"
        self.description = "Advanced downloader with best compatibility"
        self.advantages = [
            "Highest success rate",
            "Multiple quality options", 
            "Regular updates",
            "Supports watermark removal"
        ]
        self.recommended = True
        
    def download(self, url, output_path, quality="best", progress_callback=None, status_callback=None):
        """Download TikTok content using yt-dlp"""
        try:
            # Configure quality format
            format_selector = self._get_format_selector(quality)
            
            # Setup yt-dlp options
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'extractaudio': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'ignoreerrors': False,
            }
            
            # Add progress hook if provided
            if progress_callback:
                ydl_opts['progress_hooks'] = [self._progress_hook(progress_callback, status_callback)]
            
            # Download the content
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if status_callback:
                    status_callback("Extracting video information...")
                
                # Extract info first to validate
                info = ydl.extract_info(url, download=False)
                
                if status_callback:
                    status_callback(f"Downloading: {info.get('title', 'Unknown')}")
                
                # Perform actual download
                ydl.download([url])
                
                if status_callback:
                    status_callback("Download completed successfully!")
                
                return True, "Download completed successfully"
                
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            if status_callback:
                status_callback(error_msg)
            return False, error_msg
    
    def _get_format_selector(self, quality):
        """Get format selector for highest quality download"""
        # Always return the best available quality format
        # Prioritize mp4 format for compatibility, fallback to any best quality
        return "best[ext=mp4]/best"
    
    def _progress_hook(self, progress_callback, status_callback):
        """Create progress hook for yt-dlp"""
        def hook(d):
            if d['status'] == 'downloading':
                if 'total_bytes' in d and d['total_bytes']:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    progress_callback(percent)
                    if status_callback:
                        speed = d.get('speed', 0)
                        if speed:
                            speed_str = f" ({speed/1024/1024:.1f} MB/s)"
                        else:
                            speed_str = ""
                        status_callback(f"Downloading... {percent:.1f}%{speed_str}")
                        
            elif d['status'] == 'finished':
                progress_callback(100)
                if status_callback:
                    status_callback("Processing download...")
                    
        return hook
    
    def validate_url(self, url):
        """Validate if URL is supported"""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return True, info.get('title', 'Unknown content')
        except Exception as e:
            return False, str(e)
    
    def get_info(self):
        """Get engine information"""
        return {
            'name': self.name,
            'description': self.description,
            'advantages': self.advantages,
            'recommended': self.recommended
        }