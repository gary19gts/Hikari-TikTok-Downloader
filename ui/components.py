"""
Custom UI components with modern design

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

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class ModernButton(ctk.CTkButton):
    """Modern button with clean design"""
    def __init__(self, parent, **kwargs):
        # Default styling
        default_kwargs = {
            'corner_radius': 8,
            'height': 35,
            'font': ctk.CTkFont(size=13, weight="normal")
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)

class InfoTooltip:
    """Tooltip for showing information"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip:
            return
        
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#333333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=300,
            justify="left",
            padx=8,
            pady=6
        )
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ProgressBar(ctk.CTkProgressBar):
    """Modern progress bar"""
    def __init__(self, parent, **kwargs):
        default_kwargs = {
            'height': 8,
            'corner_radius': 4,
            'progress_color': "#FF0050"
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)

class StatusIndicator(ctk.CTkFrame):
    """Status indicator with colored dot"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.status_dot = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=16),
            text_color="#FF6B6B"  # Red by default
        )
        self.status_dot.pack(side="left", padx=(0, 5))
        
        self.status_text = ctk.CTkLabel(
            self,
            text="Not detected",
            font=ctk.CTkFont(size=12)
        )
        self.status_text.pack(side="left")
    
    def set_status(self, status, text):
        """Set status indicator"""
        colors = {
            "success": "#4CAF50",
            "warning": "#FF9800", 
            "error": "#FF6B6B",
            "info": "#2196F3"
        }
        
        self.status_dot.configure(text_color=colors.get(status, "#FF6B6B"))
        self.status_text.configure(text=text)