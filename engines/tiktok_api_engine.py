"""
TikTok API Engine for direct API downloads
Faster but may have limitations compared to yt-dlp

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

import requests
import re
import os
from pathlib import Path
import json

class TikTokApiEngine:
    def __init__(self):
        self.name = "tiktok-api"
        self.description = "Direct API access for faster downloads"
        self.advantages = [
            "Faster download speed",
            "Lower resource usage",
            "Direct API access",
            "Lightweight"
        ]
        self.recommended = False
        
    def download(self, url, output_path, quality="best", progress_callback=None, status_callback=None):
        """Download TikTok content using direct API"""
        try:
            if status_callback:
                status_callback("Extracting video information...")
            
            # Extract video ID from URL
            video_id = self._extract_video_id(url)
            if not video_id:
                return False, "Could not extract video ID from URL"
            
            # Get video info
            video_info = self._get_video_info(video_id)
            if not video_info:
                return False, "Could not retrieve video information"
            
            # Get download URL
            download_url = self._get_download_url(video_info, quality)
            if not download_url:
                return False, "Could not get download URL"
            
            # Download the file
            filename = self._generate_filename(video_info)
            filepath = os.path.join(output_path, filename)
            
            if status_callback:
                status_callback(f"Downloading: {video_info.get('title', 'Unknown')}")
            
            success = self._download_file(download_url, filepath, progress_callback, status_callback)
            
            if success:
                if status_callback:
                    status_callback("Download completed successfully!")
                return True, "Download completed successfully"
            else:
                return False, "Download failed"
                
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            if status_callback:
                status_callback(error_msg)
            return False, error_msg
    
    def _extract_video_id(self, url):
        """Extract TikTok video ID from URL"""
        patterns = [
            r'tiktok\.com/@[\w\.-]+/video/(\d+)',
            r'tiktok\.com/.*?/video/(\d+)',
            r'vm\.tiktok\.com/(\w+)',
            r'tiktok\.com/t/(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _get_video_info(self, video_id):
        """Get video information from TikTok API"""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd use proper TikTok API endpoints
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124'
            }
            
            # Placeholder for API call
            # Note: This would need proper TikTok API implementation
            return {
                'id': video_id,
                'title': f'TikTok_Video_{video_id}',
                'author': 'Unknown',
                'download_urls': {
                    'best': f'https://example.com/video/{video_id}.mp4'
                }
            }
            
        except Exception:
            return None
    
    def _get_download_url(self, video_info, quality):
        """Get highest quality download URL available"""
        download_urls = video_info.get('download_urls', {})
        
        # Always return the best available quality
        if 'best' in download_urls:
            return download_urls['best']
        else:
            return None
    
    def _generate_filename(self, video_info):
        """Generate safe filename for download"""
        title = video_info.get('title', 'TikTok_Video')
        # Clean filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        return f"{safe_title}.mp4"
    
    def _download_file(self, url, filepath, progress_callback=None, status_callback=None):
        """Download file with progress tracking"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            progress_callback(percent)
                            
                        if status_callback and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            status_callback(f"Downloading... {percent:.1f}%")
            
            return True
            
        except Exception:
            return False
    
    def validate_url(self, url):
        """Validate if URL is supported"""
        video_id = self._extract_video_id(url)
        if video_id:
            return True, f"TikTok video detected (ID: {video_id})"
        else:
            return False, "Invalid TikTok URL format"
    
    def get_info(self):
        """Get engine information"""
        return {
            'name': self.name,
            'description': self.description,
            'advantages': self.advantages,
            'recommended': self.recommended
        }