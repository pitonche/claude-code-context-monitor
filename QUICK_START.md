# Quick Start Guide

## Run the Monitor

```bash
# Option 1: Use the launcher (Windows)
run.bat

# Option 2: Direct Python command
python src\main.py

# Option 3: Python module (cross-platform)
python -m src.main
```

## What You'll See

```
┌─────────────────────────────────┐
│  Claude Code Tokens        [×]  │
│                                 │
│          85.2%                  │  ← GREEN/AMBER/ORANGE/RED
│      ███████████░░░             │  ← Progress bar
│                                 │
│   75,120 / 88,000 tokens        │  ← Current / Limit
│        [Max5 Plan]              │  ← Your plan
│                                 │
│    [Compress Context]           │  ← Enabled at 70%+
└─────────────────────────────────┘
```

## Using the Compress Button

1. Wait until usage reaches **70%** (61,600+ tokens)
2. Button turns **green** and becomes clickable
3. Click button
4. Command `/compress` is **copied to clipboard**
5. Paste into Claude Code terminal
6. Context compresses, token count drops

## Color Meanings

🟢 **Green (0-70%)**: You're safe, keep working
🟡 **Amber (70-90%)**: Consider compressing soon
🟠 **Orange (90-95%)**: Compress recommended
🔴 **Red (95-100%+)**: Compress immediately!

## Common Issues

**"No active session" displayed**
- Start a Claude Code session first
- Monitor will auto-detect within 2 seconds

**Window appears off-screen**
- Delete: `%USERPROFILE%\.claude-monitor\position.json`
- Restart monitor (will center on screen)

**Button won't enable**
- Generate more tokens (need 70%+ usage)
- Check percentage display

**Python not found**
- Install Python 3.8+ from python.org
- Ensure "Add to PATH" was checked

## Customization

Edit `src/config.py`:

```python
# Change plan limit
PLAN_LIMIT = PlanLimits.PRO      # 44k (Pro)
PLAN_LIMIT = PlanLimits.MAX5     # 88k (Max5) ← DEFAULT
PLAN_LIMIT = PlanLimits.MAX20    # 220k (Max20)

# Change refresh rate
REFRESH_INTERVAL_MS = 2000  # 2 seconds ← DEFAULT
REFRESH_INTERVAL_MS = 1000  # 1 second (more responsive)

# Change compress threshold
COMPRESS_THRESHOLD = 70.0   # Enable at 70% ← DEFAULT
COMPRESS_THRESHOLD = 80.0   # Enable at 80%
```

## Keyboard Shortcuts

- **Click + Drag**: Move window
- **Close (X)**: Save position and quit
- **Alt+F4**: Quit (Windows)

## File Locations

```
Monitor reads:  ~/.claude/projects/**/*.jsonl
Monitor writes: ~/.claude-monitor/position.json
```

## Test the Monitor

```bash
# Run unit tests
run_tests.bat

# Or manually
python tests\test_token_calculator.py
python tests\test_data_reader.py
```

## Performance

- Memory: ~15 MB
- CPU: < 1%
- Updates: Every 2 seconds
- Startup: < 500ms

## Get Help

- General usage → README.md
- Installation → INSTALL.md
- Technical details → ARCHITECTURE.md
- Version history → CHANGELOG.md
- This summary → IMPLEMENTATION_SUMMARY.md

## That's It!

The monitor is running. Just use Claude Code normally and watch your token usage in real-time.

**Pro tip**: Position the window in a corner where you can always see it without blocking your work area.
