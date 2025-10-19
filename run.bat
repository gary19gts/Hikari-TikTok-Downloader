@echo off
REM Hikari TikTok Downloader Launcher Script
REM Copyright (C) 2025 Gary19gts
REM 
REM This program is dual-licensed:
REM 1. GNU Affero General Public License v3 (AGPLv3) for open source use
REM 2. Proprietary license for commercial/closed source use
REM 
REM For commercial licensing, contact Gary19gts.
REM Author: Gary19gts

title Hikari TikTok Downloader - by Gary19gts
echo.
echo ========================================
echo   Hikari TikTok Downloader - by Gary19gts
echo   Version: v1.2.0
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Run the launcher
python run.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application closed with an error.
    pause
)