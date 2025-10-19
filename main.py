#!/usr/bin/env python3
"""
Hikari TikTok Downloader
A modern TikTok content downloader with clean UI

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
Version: 1.2.0
Date: October 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import os
import sys
import json
from pathlib import Path
import webbrowser
from datetime import datetime

# Import downloader engines
from engines.yt_dlp_engine import YtDlpEngine
from engines.tiktok_api_engine import TikTokApiEngine
from ui.components import ModernButton, InfoTooltip, ProgressBar
from ui.styles import ModernStyle
from utils.validator import URLValidator
from utils.logger import Logger

class HikariTikTokDownloader:
    def __init__(self):
        # Initialize CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        # Set white background
        self.root.configure(fg_color="white")
        
        self.setup_window()
        self.setup_variables()
        self.setup_engines()
        self.create_ui()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("Hikari TikTok Downloader v1.2.0 - by Gary19gts")
        self.root.geometry("720x700")
        self.root.minsize(720, 700)
        
        # Set window icon
        try:
            if os.path.exists("hikari_icon.ico"):
                self.root.iconbitmap("hikari_icon.ico")
            elif os.path.exists("hikari_icon.png"):
                icon_image = Image.open("hikari_icon.png")
                icon_photo = ImageTk.PhotoImage(icon_image.resize((32, 32)))
                self.root.iconphoto(True, icon_photo)
        except Exception:
            pass  # Continue without icon if there's an error
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (720 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"720x700+{x}+{y}")
        
    def setup_variables(self):
        """Initialize variables"""
        self.url_var = tk.StringVar()
        
        # Settings file path
        self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
        
        # Create Downloads folder in program directory (default)
        self.default_downloads_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Downloads")
        if not os.path.exists(self.default_downloads_path):
            try:
                os.makedirs(self.default_downloads_path)
            except Exception:
                self.default_downloads_path = os.getcwd()  # Fallback to current directory
        
        # Load settings or use defaults
        settings = self.load_settings()
        last_output_dir = settings.get("last_output_dir", self.default_downloads_path)
        
        # Verify the last output directory still exists
        if not os.path.exists(last_output_dir):
            last_output_dir = self.default_downloads_path
        
        self.output_dir = tk.StringVar(value=last_output_dir)
        self.engine_var = tk.StringVar(value=settings.get("engine", "yt-dlp"))
        self.quality_var = tk.StringVar(value="best")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        self.logger = Logger()
        self.validator = URLValidator()
        
    def setup_engines(self):
        """Initialize download engines"""
        self.engines = {
            "yt-dlp": YtDlpEngine(),
            "tiktok-api": TikTokApiEngine()
        }
        
    def create_ui(self):
        """Create the main user interface"""
        # Main container with white background
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create two columns
        self.create_left_column(main_frame)
        self.create_right_column(main_frame)
        
    def create_left_column(self, parent):
        """Create left column with main controls"""
        left_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="#F8F9FA")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Title
        title_label = ctk.CTkLabel(
            left_frame, 
            text="Hikari TikTok Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Disclaimer
        disclaimer_frame = ctk.CTkFrame(left_frame, fg_color="#FFF3CD", corner_radius=10)
        disclaimer_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        disclaimer_text = ctk.CTkLabel(
            disclaimer_frame,
            text="⚠️ IMPORTANT: Only download your own content or content you have permission to download.",
            font=ctk.CTkFont(size=12),
            text_color="#856404",
            wraplength=300
        )
        disclaimer_text.pack(pady=10, padx=10)
        
        # URL Input Section
        self.create_url_section(left_frame)
        
        # Engine Selection
        self.create_engine_section(left_frame)
        
        # Quality Selection
        self.create_quality_section(left_frame)
        
        # Output Directory
        self.create_output_section(left_frame)
        
        # Download Button
        self.create_download_section(left_frame)
        
    def create_right_column(self, parent):
        """Create right column with status and diagnostics"""
        right_frame = ctk.CTkFrame(parent, corner_radius=15, fg_color="#F8F9FA", width=280)
        right_frame.pack(side="right", fill="both", padx=(15, 0))
        right_frame.pack_propagate(False)  # Maintain fixed width
        
        # Content Detector
        self.create_detector_section(right_frame)
        
        # Progress Section
        self.create_progress_section(right_frame)
        
        # Support Development Section
        self.create_support_section(right_frame)
        
        # Credits
        self.create_credits_section(right_frame)
        
    def create_url_section(self, parent):
        """Create URL input section"""
        url_frame = ctk.CTkFrame(parent, fg_color="transparent")
        url_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        url_label = ctk.CTkLabel(url_frame, text="TikTok URL:", font=ctk.CTkFont(size=14, weight="bold"))
        url_label.pack(anchor="w")
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            placeholder_text="Paste TikTok URL here...",
            height=35,
            corner_radius=8
        )
        self.url_entry.pack(fill="x", pady=(5, 0))
        self.url_entry.bind("<KeyRelease>", self.on_url_change)
        
    def create_engine_section(self, parent):
        """Create engine selection section"""
        engine_frame = ctk.CTkFrame(parent, fg_color="transparent")
        engine_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        engine_label = ctk.CTkLabel(engine_frame, text="Download Engine:", font=ctk.CTkFont(size=14, weight="bold"))
        engine_label.pack(anchor="w")
        
        engine_control_frame = ctk.CTkFrame(engine_frame, fg_color="transparent")
        engine_control_frame.pack(fill="x", pady=(5, 0))
        
        self.engine_combo = ctk.CTkComboBox(
            engine_control_frame,
            variable=self.engine_var,
            values=["yt-dlp", "tiktok-api"],
            height=30,
            corner_radius=8,
            state="readonly"
        )
        self.engine_combo.pack(side="left", fill="x", expand=True)
        
        # Info button for engines
        info_btn = ctk.CTkButton(
            engine_control_frame,
            text="ℹ️",
            width=30,
            height=30,
            corner_radius=15,
            command=self.show_engine_info
        )
        info_btn.pack(side="right", padx=(5, 0))
        
    def create_quality_section(self, parent):
        """Create quality selection section"""
        quality_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quality_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        quality_label = ctk.CTkLabel(quality_frame, text="Quality:", font=ctk.CTkFont(size=14, weight="bold"))
        quality_label.pack(anchor="w")
        
        quality_control_frame = ctk.CTkFrame(quality_frame, fg_color="transparent")
        quality_control_frame.pack(fill="x", pady=(5, 0))
        
        self.quality_combo = ctk.CTkComboBox(
            quality_control_frame,
            variable=self.quality_var,
            values=["best"],
            height=30,
            corner_radius=8,
            state="readonly"
        )
        self.quality_combo.pack(side="left", fill="x", expand=True)
        
        # Info button for quality
        quality_info_btn = ctk.CTkButton(
            quality_control_frame,
            text="ℹ️",
            width=30,
            height=30,
            corner_radius=15,
            command=self.show_quality_info
        )
        quality_info_btn.pack(side="right", padx=(5, 0))
        
    def create_output_section(self, parent):
        """Create output directory section"""
        output_frame = ctk.CTkFrame(parent, fg_color="transparent")
        output_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        output_label = ctk.CTkLabel(output_frame, text="Output Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        output_label.pack(anchor="w")
        
        output_control_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_control_frame.pack(fill="x", pady=(5, 0))
        
        self.output_entry = ctk.CTkEntry(
            output_control_frame,
            textvariable=self.output_dir,
            height=30,
            corner_radius=8
        )
        self.output_entry.pack(side="left", fill="x", expand=True)
        
        default_btn = ctk.CTkButton(
            output_control_frame,
            text="Default",
            width=65,
            height=30,
            corner_radius=8,
            command=self.set_default_folder
        )
        default_btn.pack(side="right", padx=(5, 0))
        
        browse_btn = ctk.CTkButton(
            output_control_frame,
            text="Browse",
            width=70,
            height=30,
            corner_radius=8,
            command=self.browse_output_folder
        )
        browse_btn.pack(side="right", padx=(5, 0))
        
        open_btn = ctk.CTkButton(
            output_control_frame,
            text="Open",
            width=60,
            height=30,
            corner_radius=8,
            command=self.open_output_folder
        )
        open_btn.pack(side="right", padx=(5, 0))
        
    def create_download_section(self, parent):
        """Create download button section"""
        download_frame = ctk.CTkFrame(parent, fg_color="transparent")
        download_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Main download button
        self.download_btn = ctk.CTkButton(
            download_frame,
            text="Download Content",
            height=45,
            corner_radius=12,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#FF0050",  # TikTok pink
            hover_color="#E6004A",
            text_color="white",  # White text color
            text_color_disabled="white",  # White text when disabled
            command=self.start_download
        )
        self.download_btn.pack(fill="x", pady=(0, 10))
        
        # Update libraries button
        self.update_btn = ctk.CTkButton(
            download_frame,
            text="Update Libraries",
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#FF0050",  # TikTok Pink
            hover_color="#E6004A",
            text_color="white",  # White text color
            command=self.update_libraries
        )
        self.update_btn.pack(fill="x")
    
    def create_detector_section(self, parent):
        """Create content detector section"""
        detector_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
        detector_frame.pack(fill="x", padx=15, pady=(20, 12))
        
        detector_label = ctk.CTkLabel(
            detector_frame,
            text="Content Detector",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        detector_label.pack(pady=(15, 5))
        
        from ui.components import StatusIndicator
        self.status_indicator = StatusIndicator(detector_frame, fg_color="transparent")
        self.status_indicator.pack(pady=(0, 15))
        
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
        progress_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        progress_label = ctk.CTkLabel(
            progress_frame,
            text="Download Progress",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        progress_label.pack(pady=(15, 5))
        
        from ui.components import ProgressBar
        self.progress_bar = ProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 5))
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        self.status_label.pack(pady=(0, 15))
        
    def create_support_section(self, parent):
        """Create support development section"""
        support_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
        support_frame.pack(fill="x", padx=12, pady=(0, 18))
        
        support_label = ctk.CTkLabel(
            support_frame,
            text="☕ Support Development",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        support_label.pack(pady=(20, 8))
        
        support_text = ctk.CTkLabel(
            support_frame,
            text="If you find Hikari useful, consider\nsupporting its development!",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            justify="center"
        )
        support_text.pack(pady=(0, 15))
        
        # Ko-fi button
        kofi_btn = ctk.CTkButton(
            support_frame,
            text="☕ Buy me a coffee on Ko-fi",
            height=40,
            corner_radius=10,
            fg_color="#FF5E5B",  # Ko-fi red color
            hover_color="#E54B47",
            text_color="white",  # Explicit white text color
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.open_kofi
        )
        kofi_btn.pack(fill="x", padx=18, pady=(0, 15))
        
        thanks_label = ctk.CTkLabel(
            support_frame,
            text="Thank you for your support! 🖤",
            font=ctk.CTkFont(size=11),
            text_color="#999999"
        )
        thanks_label.pack(pady=(0, 20))
        
    def create_credits_section(self, parent):
        """Create credits section"""
        credits_frame = ctk.CTkFrame(parent, corner_radius=10, fg_color="white")
        credits_frame.pack(fill="x", padx=12, pady=(0, 20))
        
        credits_label = ctk.CTkLabel(
            credits_frame,
            text="Credits",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        credits_label.pack(pady=(18, 8))
        
        app_info = ctk.CTkLabel(
            credits_frame,
            text="Hikari TikTok Downloader\nv1.2.0\nOctober 2025\n\nMade by: Gary19gts",
            font=ctk.CTkFont(size=11),
            text_color="#666666",
            justify="center"
        )
        app_info.pack(pady=(0, 12))
        
        # Credits button
        credits_btn = ctk.CTkButton(
            credits_frame,
            text="Special Thanks",
            width=120,
            height=32,
            corner_radius=8,
            command=self.show_credits
        )
        credits_btn.pack(pady=(0, 18))
        
    # Event handlers and utility methods
    def on_url_change(self, event=None):
        """Handle URL input change"""
        url = self.url_var.get().strip()
        if url:
            is_valid, message = self.validator.is_valid_tiktok_url(url)
            if is_valid:
                self.status_indicator.set_status("success", "Content detected")
                self.logger.info(f"Valid URL detected: {url}")
            else:
                self.status_indicator.set_status("error", "No content detected")
                self.logger.warning(f"Invalid URL: {message}")
        else:
            self.status_indicator.set_status("error", "No content detected")
    
    def show_engine_info(self):
        """Show engine information tooltip"""
        engine_name = self.engine_var.get()
        engine = self.engines.get(engine_name)
        
        if engine:
            info = engine.get_info()
            advantages_text = "\n• ".join(info['advantages'])
            recommended_text = " (Recommended)" if info['recommended'] else ""
            
            message = f"{info['description']}{recommended_text}\n\nAdvantages:\n• {advantages_text}"
            messagebox.showinfo(f"{info['name']} Engine", message)
    
    def show_quality_info(self):
        """Show quality information"""
        message = "Downloads in the highest available quality (up to 1080p)\n\nThis ensures you get the best possible video quality with optimal file size."
        messagebox.showinfo("Quality Information", message)
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.output_dir.get()
        )
        if folder:
            self.output_dir.set(folder)
            self.save_settings()  # Save the new folder selection
            self.logger.info(f"Output folder changed to: {folder}")
    
    def set_default_folder(self):
        """Set output folder to default Downloads folder"""
        self.output_dir.set(self.default_downloads_path)
        self.save_settings()
        self.logger.info(f"Output folder reset to default: {self.default_downloads_path}")
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Could not load settings: {e}")
        return {}
    
    def save_settings(self):
        """Save current settings to JSON file"""
        try:
            settings = {
                "last_output_dir": self.output_dir.get(),
                "engine": self.engine_var.get(),
                "quality": self.quality_var.get()
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            self.logger.debug("Settings saved successfully")
        except Exception as e:
            self.logger.warning(f"Could not save settings: {e}")
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_path = self.output_dir.get()
        if os.path.exists(output_path):
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                os.system(f"open '{output_path}'")
            else:
                os.system(f"xdg-open '{output_path}'")
        else:
            messagebox.showerror("Error", "Output folder does not exist")
    
    def start_download(self):
        """Start download process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a TikTok URL")
            return
        
        # Validate URL
        is_valid, message = self.validator.is_valid_tiktok_url(url)
        if not is_valid:
            messagebox.showerror("Invalid URL", message)
            return
        
        # Check output directory
        output_path = self.output_dir.get()
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {e}")
                return
        
        # Disable download button
        self.download_btn.configure(state="disabled", text="Downloading...")
        
        # Start download in separate thread
        download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, output_path),
            daemon=True
        )
        download_thread.start()
    
    def _download_worker(self, url, output_path):
        """Download worker thread"""
        try:
            engine_name = self.engine_var.get()
            engine = self.engines.get(engine_name)
            quality = self.quality_var.get()
            
            self.logger.info(f"Starting download with {engine_name} engine")
            self.logger.info(f"URL: {url}")
            self.logger.info(f"Quality: {quality}")
            self.logger.info(f"Output: {output_path}")
            
            # Progress callback
            def progress_callback(percent):
                self.root.after(0, lambda: self.progress_bar.set(percent / 100))
            
            # Status callback
            def status_callback(status):
                self.root.after(0, lambda: self.status_var.set(status))
            
            # Perform download
            success, message = engine.download(
                url, output_path, quality, 
                progress_callback, status_callback
            )
            
            # Update UI on main thread
            self.root.after(0, lambda: self._download_complete(success, message))
            
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            self.logger.error(error_msg)
            self.root.after(0, lambda: self._download_complete(False, error_msg))
    
    def _download_complete(self, success, message):
        """Handle download completion"""
        # Re-enable download button
        self.download_btn.configure(state="normal", text="Download Content")
        
        if success:
            self.progress_bar.set(1.0)
            self.status_var.set("Download completed!")
            self.logger.info("Download completed successfully")
            messagebox.showinfo("Success", message)
        else:
            self.progress_bar.set(0)
            self.status_var.set("Download failed")
            self.logger.error(f"Download failed: {message}")
            messagebox.showerror("Download Failed", message)
    
    def show_diagnostics(self):
        """Show diagnostics window"""
        diag_window = ctk.CTkToplevel(self.root)
        diag_window.title("Diagnostics - Hikari TikTok Downloader")
        diag_window.geometry("600x400")
        
        # Log display
        log_frame = ctk.CTkFrame(diag_window)
        log_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="Recent Logs",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        log_label.pack(pady=(10, 5))
        
        # Text widget for logs
        log_text = ctk.CTkTextbox(log_frame, wrap="word")
        log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load recent logs
        recent_logs = self.logger.get_recent_logs()
        if recent_logs:
            log_text.insert("1.0", "\n".join(recent_logs))
        else:
            log_text.insert("1.0", "No logs available")
        
        # Buttons
        button_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="Refresh",
            command=lambda: self._refresh_logs(log_text)
        )
        refresh_btn.pack(side="left", padx=(0, 5))
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Logs",
            command=lambda: self._clear_logs(log_text)
        )
        clear_btn.pack(side="left")
    
    def _refresh_logs(self, log_text):
        """Refresh log display"""
        log_text.delete("1.0", "end")
        recent_logs = self.logger.get_recent_logs()
        if recent_logs:
            log_text.insert("1.0", "\n".join(recent_logs))
        else:
            log_text.insert("1.0", "No logs available")
    
    def _clear_logs(self, log_text):
        """Clear logs"""
        self.logger.clear_logs()
        log_text.delete("1.0", "end")
        log_text.insert("1.0", "Logs cleared")
    
    def show_credits(self):
        """Show credits and acknowledgments window"""
        credits_window = ctk.CTkToplevel(self.root)
        credits_window.title("Credits & Acknowledgments")
        credits_window.geometry("500x600")
        credits_window.configure(fg_color="white")
        
        # Main frame
        main_frame = ctk.CTkFrame(credits_window, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Credits & Acknowledgments",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#333333"
        )
        title_label.pack(pady=(10, 20))
        
        # Scrollable frame for credits
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F8F9FA")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Developer section
        dev_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="white")
        dev_frame.pack(fill="x", pady=(0, 15))
        
        dev_title = ctk.CTkLabel(
            dev_frame,
            text="🧑‍💻 Developer",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF0050"
        )
        dev_title.pack(pady=(15, 5))
        
        dev_info = ctk.CTkLabel(
            dev_frame,
            text="Gary19gts\nCreator of Hikari TikTok Downloader\n\nThank you for using this application!\nBuilt with passion for the community.",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            justify="center"
        )
        dev_info.pack(pady=(0, 15))
        
        # Libraries section
        lib_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="white")
        lib_frame.pack(fill="x", pady=(0, 15))
        
        lib_title = ctk.CTkLabel(
            lib_frame,
            text="📚 Libraries & Dependencies",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#007AFF"
        )
        lib_title.pack(pady=(15, 10))
        
        libraries_text = """🎨 CustomTkinter
Modern and customizable tkinter library
Created by Tom Schimansky
Provides the beautiful modern interface

🖼️ Pillow (PIL)
Python Imaging Library
Image processing capabilities
Essential for GUI graphics

📥 yt-dlp
Universal video downloader
Fork of youtube-dl with active development
The most reliable TikTok download engine

🌐 Requests
HTTP library for Python
Simple and elegant HTTP requests
Used for API communications

🐍 Python
The programming language that powers it all
Created by Guido van Rossum
Foundation of this entire application"""
        
        lib_info = ctk.CTkLabel(
            lib_frame,
            text=libraries_text,
            font=ctk.CTkFont(size=11),
            text_color="#666666",
            justify="left"
        )
        lib_info.pack(pady=(0, 15), padx=15)
        
        # Special thanks section
        thanks_frame = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="white")
        thanks_frame.pack(fill="x", pady=(0, 15))
        
        thanks_title = ctk.CTkLabel(
            thanks_frame,
            text="🙏 Special Thanks",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#34C759"
        )
        thanks_title.pack(pady=(15, 5))
        
        thanks_text = ctk.CTkLabel(
            thanks_frame,
            text="• Open source community for amazing tools\n• TikTok for creating an engaging platform\n• All users who respect content creators' rights\n• Contributors to the libraries we depend on\n• Everyone who uses this tool responsibly",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            justify="left"
        )
        thanks_text.pack(pady=(0, 15), padx=15)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            height=35,
            corner_radius=8,
            fg_color="#FF0050",
            hover_color="#E6004A",
            command=credits_window.destroy
        )
        close_btn.pack(pady=(10, 0))
    
    def open_kofi(self):
        """Open Ko-fi support page"""
        kofi_url = "https://ko-fi.com/gary19gts"
        try:
            webbrowser.open(kofi_url)
            self.logger.info("Opened Ko-fi support page")
        except Exception as e:
            self.logger.error(f"Failed to open Ko-fi page: {e}")
            messagebox.showerror("Error", "Could not open Ko-fi page. Please visit: https://ko-fi.com/gary19gts")
    
    def update_libraries(self):
        """Update libraries automatically"""
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Update Libraries",
            "This will update all libraries to their latest versions.\n\nThis may take a few minutes. Continue?",
            icon="question"
        )
        
        if not result:
            return
        
        # Disable update button during process
        self.update_btn.configure(state="disabled", text="Updating...")
        
        # Start update in separate thread
        update_thread = threading.Thread(
            target=self._update_worker,
            daemon=True
        )
        update_thread.start()
    
    def _update_worker(self):
        """Update worker thread"""
        try:
            import subprocess
            
            self.logger.info("Starting library update process")
            
            # List of libraries to update
            libraries = [
                "customtkinter",
                "pillow", 
                "yt-dlp",
                "requests"
            ]
            
            # Update each library
            for lib in libraries:
                self.root.after(0, lambda l=lib: self.status_var.set(f"Updating {l}..."))
                self.logger.info(f"Updating {lib}")
                
                try:
                    # Run pip install --upgrade for each library
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", "--upgrade", lib
                    ], capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        self.logger.info(f"Successfully updated {lib}")
                    else:
                        self.logger.warning(f"Failed to update {lib}: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    self.logger.error(f"Timeout updating {lib}")
                except Exception as e:
                    self.logger.error(f"Error updating {lib}: {e}")
            
            # Update UI on main thread
            self.root.after(0, self._update_complete)
            
        except Exception as e:
            error_msg = f"Update failed: {str(e)}"
            self.logger.error(error_msg)
            self.root.after(0, lambda: self._update_complete(False, error_msg))
    
    def _update_complete(self, success=True, message=""):
        """Handle update completion"""
        # Re-enable update button
        self.update_btn.configure(state="normal", text="Update Libraries")
        
        if success:
            self.status_var.set("Libraries updated successfully!")
            self.logger.info("Library update completed successfully")
            messagebox.showinfo(
                "Update Complete", 
                "Libraries have been updated successfully!\n\nRestart the application to use the latest versions."
            )
        else:
            self.status_var.set("Update failed")
            self.logger.error(f"Library update failed: {message}")
            messagebox.showerror("Update Failed", f"Library update failed:\n\n{message}")
        
    def run(self):
        """Start the application"""
        self.logger.info("Hikari TikTok Downloader started")
        
        # Save settings when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        self.save_settings()
        self.logger.info("Hikari TikTok Downloader closed")
        self.root.destroy()

if __name__ == "__main__":
    app = HikariTikTokDownloader()
    app.run()