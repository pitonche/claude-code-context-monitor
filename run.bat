@echo off
REM Launch script for Claude Code Odometer Monitor

echo Starting Claude Code Odometer Monitor...
py src\main.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the monitor.
    echo Please ensure Python 3.8+ is installed and in your PATH.
    pause
)
