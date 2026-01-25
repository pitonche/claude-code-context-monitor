@echo off
REM Auto-launch script for Claude Code Odometer Monitor
REM This script is designed to be called from Claude Code's SessionStart hook

REM Launch monitor in background (no console window)
REM Python lock file handles duplicate prevention
REM Change this path to match your installation directory
cd /d %~dp0
start "" pythonw src\main.py

exit /b 0
