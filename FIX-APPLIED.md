# Blocking Issue - FIX ATTEMPTS

## Attempt #1: Non-Blocking Hook + Remove Startup Wait ❌ FAILED

## Problem
When launching Claude Code with `clauded`, the Context Monitor appeared but Claude Code did not appear in the terminal. User had to either close the monitor (then Claude Code instantly appeared) or start a new terminal.

## Root Cause
Two blocking issues were identified:

1. **Hook Command Blocking** (5 seconds)
   - SessionStart hook used: `cmd /c ~/.claude/launch-odometer.bat`
   - Hook had `timeout: 5` which meant Claude Code waited up to 5 seconds
   - The command wasn't truly asynchronous

2. **Monitor Startup Blocking** (6.5 seconds)
   - `wait_for_session()` in main.py:187 blocked for up to 6.5 seconds
   - 1.5s initial delay + 10 retries × 500ms = 6.5 seconds total
   - This blocking happened during the SessionStart hook, preventing Claude Code from initializing

## Solution Applied

### Fix 1: Non-Blocking Hook Command
Changed the SessionStart hook from:
```json
{
  "type": "command",
  "command": "cmd /c ~/.claude/launch-odometer.bat",
  "timeout": 5
}
```

To:
```json
{
  "type": "command",
  "command": "start /B /MIN cmd /c ~/.claude/launch-odometer.bat"
}
```

Changes:
- `start /B` - Runs in background without creating new window (non-blocking)
- `/MIN` - Minimizes any console windows
- Removed `timeout: 5` - Not needed since command returns immediately

### Fix 2: Removed Blocking Wait
Modified `src/main.py` line 184-187:

**Before:**
```python
# Initialize odometer widget
odometer = OdometerWidget(root)

# Wait for session file to appear
wait_for_session()  # Wait for up to ~6.5 seconds

# Initialize compress handler
```

**After:**
```python
# Initialize odometer widget
odometer = OdometerWidget(root)

# Initialize compress handler
```

The monitor now starts immediately and shows "No active session" until Claude Code creates the session file. The refresh loop (every 2 seconds) handles detecting the session automatically.

## Testing

1. Close all existing Context Monitor instances
2. Run: `clauded`
3. Expected result: Both monitor and Claude Code appear instantly and simultaneously
4. Monitor initially shows "No active session", then updates within 2 seconds once Claude Code is ready

## Files Modified

- `~/.claude/settings.json` - Updated SessionStart hook
- `src/main.py` - Removed blocking wait

## Why This Should Have Worked (But Didn't)

- **No Hook Timeout**: The hook returns instantly because `start /B` launches the batch file asynchronously
- **No Startup Blocking**: The monitor starts immediately without waiting for session files
- **Automatic Detection**: The 2-second refresh loop finds the session file automatically
- **Clean Separation**: Claude Code and Monitor run as independent processes from the start

**Result**: Still blocked. The SessionStart hook approach appears fundamentally incompatible with the user's `clauded` alias setup.

---

## Attempt #2: Wrapper Script (No Hook) ⏳ TESTING

### Strategy
Completely abandon the SessionStart hook approach. Instead:
1. **Remove the SessionStart hook entirely**
2. **Create a wrapper script** that launches both monitor and Claude Code
3. **Replace the `clauded` alias** to point to the wrapper script

This gives us full control over the launch sequence without relying on Claude Code's hook system.

### Implementation

**Created Files:**
- `clauded-wrapper.bat` - Launches monitor, then Claude Code with --bypass-permissions
- `disable-hook.ps1` - Removes SessionStart hook from settings.json

**Wrapper Script Logic:**
```batch
# Launch monitor (background, non-blocking)
start "" /MIN pythonw "path\to\claude-code-context-monitor\src\main.py"

# Launch Claude Code with --bypass-permissions
claude.exe --bypass-permissions %*
```

**Hook Status:** Disabled (removed from settings.json)

### Setup Instructions

1. The SessionStart hook has been removed from `~/.claude/settings.json`
2. Use the wrapper script at: `E:\10_CLAUDE_CODE\12_CC_ContextMonitor\clauded-wrapper.bat`
3. Update your `clauded` alias to point to the wrapper script

### How to Update Your Alias

You need to find where your current `clauded` alias is defined and replace it. Common locations:

**Option A: PowerShell Profile**
```powershell
# Edit: $PROFILE
function clauded { & "path\to\claude-code-context-monitor\clauded-wrapper.bat" $args }
```

**Option B: Batch File Alias**
If you have a `clauded.bat` somewhere in your PATH:
```batch
@echo off
path\to\claude-code-context-monitor\clauded-wrapper.bat %*
```

**Option C: DOSKEY Macro** (in AutoRun script)
```batch
doskey clauded=path\to\claude-code-context-monitor\clauded-wrapper.bat $*
```

**Option D: Add to PATH**
Add `path\to\claude-code-context-monitor\` to your PATH and rename `clauded-wrapper.bat` to `clauded.bat`

### Testing
1. Close all existing Context Monitor instances
2. Close this Claude Code session
3. Open a new terminal
4. Run: `clauded`
5. Expected: Monitor appears in background, Claude Code appears in terminal immediately

### Files Modified
- `~/.claude/settings.json` - SessionStart hook removed
- Created: `clauded-wrapper.bat` - New launcher script
- Created: `disable-hook.ps1` - Hook removal script
