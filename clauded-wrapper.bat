@echo off
REM Wrapper script to launch Context Monitor + Claude Code
REM This replaces your 'clauded' alias to avoid SessionStart hook blocking

REM Launch monitor in background (completely async, no waiting)
REM IMPORTANT: Update this path to match your installation directory
start "" /MIN pythonw "%~dp0src\main.py"

REM Launch Claude Code with all arguments passed through
REM The --dangerously-skip-permissions flag is included here (matches typical alias)
REM Update claude.exe path if needed (this assumes it's in PATH)
claude.exe --dangerously-skip-permissions %*

REM Exit code from Claude Code
exit /b %ERRORLEVEL%
