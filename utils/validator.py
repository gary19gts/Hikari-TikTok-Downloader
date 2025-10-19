"""
URL validation utilities

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

import re
from urllib.parse import urlparse

class URLValidator:
    """Validates TikTok URLs"""
    
    TIKTOK_PATTERNS = [
        r'https?://(?:www\.)?tiktok\.com/@[\w\.-]+/video/\d+',
        r'https?://(?:www\.)?tiktok\.com/.*?/video/\d+',
        r'https?://vm\.tiktok\.com/\w+',
        r'https?://(?:www\.)?tiktok\.com/t/\w+',
        r'https?://m\.tiktok\.com/.*',
    ]
    
    def is_valid_tiktok_url(self, url):
        """Check if URL is a valid TikTok URL"""
        if not url or not isinstance(url, str):
            return False, "URL is empty or invalid"
        
        # Basic URL validation
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"
        except Exception:
            return False, "Invalid URL format"
        
        # Check if it's a TikTok domain
        if 'tiktok.com' not in parsed.netloc.lower():
            return False, "URL is not from TikTok"
        
        # Check against known patterns
        for pattern in self.TIKTOK_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True, "Valid TikTok URL detected"
        
        return False, "URL format not recognized"
    
    def extract_video_id(self, url):
        """Extract video ID from TikTok URL"""
        patterns = [
            r'tiktok\.com/@[\w\.-]+/video/(\d+)',
            r'tiktok\.com/.*?/video/(\d+)',
            r'vm\.tiktok\.com/(\w+)',
            r'tiktok\.com/t/(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def normalize_url(self, url):
        """Normalize TikTok URL to standard format"""
        if not url:
            return url
        
        # Add https if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url