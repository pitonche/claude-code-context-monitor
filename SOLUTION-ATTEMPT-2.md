# Solution Attempt #2: Wrapper Script Approach

## What We Did

Instead of trying to make the SessionStart hook work, we completely bypassed it and created a wrapper script that YOU control through your PowerShell alias.

### Changes Made

1. **Disabled SessionStart Hook** ✓
   - Removed from `~/.claude/settings.json`
   - No more hook blocking issues

2. **Created Wrapper Script** ✓
   - File: `clauded-wrapper.bat`
   - Launches monitor in background with `start "" /MIN pythonw`
   - Then launches Claude Code with `--dangerously-skip-permissions`
   - Monitor and Claude Code are completely independent

3. **Updated PowerShell Profile** ✓
   - File: `$PROFILE` (typically in `Documents\WindowsPowerShell\`)
   - Backup created automatically with timestamp

   **Old function:**
   ```powershell
   function clauded {
       claude --dangerously-skip-permissions @args
   }
   ```

   **New function:**
   ```powershell
   function clauded {
       # Launch Context Monitor + Claude Code via wrapper script
       & "path\to\claude-code-context-monitor\clauded-wrapper.bat" @args
   }
   ```

## How It Works Now

```
You type: clauded
    ↓
PowerShell calls: clauded-wrapper.bat
    ↓
    ├─→ Launches monitor (background, non-blocking)
    │   start "" /MIN pythonw path\to\src\main.py
    │   (Returns immediately)
    │
    └─→ Launches Claude Code (foreground, interactive)
        claude.exe --dangerously-skip-permissions
        (Your terminal session)
```

## Testing Instructions

1. **Close this Claude Code session** (important - need to reload PowerShell profile)
2. **Open a new terminal window** (loads updated PowerShell profile)
3. **Run:** `clauded`
4. **Expected result:**
   - Monitor window appears in background (minimized/quiet)
   - Claude Code appears in terminal immediately
   - Both running independently

## If It Still Doesn't Work

If you still see blocking, check:

1. **Is the PowerShell profile loaded?**
   ```powershell
   Get-Command clauded | Select-Object -ExpandProperty Definition
   ```
   Should show the new wrapper path.

2. **Does the wrapper work directly?**
   ```batch
   path\to\claude-code-context-monitor\clauded-wrapper.bat
   ```
   If this works but `clauded` doesn't, the profile didn't reload.

3. **Try force-reloading the profile:**
   ```powershell
   . $PROFILE
   ```

## Files Modified

- `~/.claude/settings.json` - SessionStart hook removed
- `$PROFILE` - Updated clauded function
- Created: `clauded-wrapper.bat` - New launcher
- Created: `disable-hook.ps1` - Hook removal script
- Created: `update-powershell-profile.ps1` - Profile updater script
- Created: `find-clauded-alias.ps1` - Alias discovery script

## Rollback Instructions

If you want to revert to the old setup:

1. Restore PowerShell profile backup:
   ```powershell
   # Find backup files with:
   Get-ChildItem (Split-Path $PROFILE) -Filter "*.backup_*"

   # Restore the backup:
   Copy-Item "path\to\backup\file" $PROFILE -Force
   ```

2. (Optional) Re-enable SessionStart hook in `~/.claude/settings.json`

## Why This Should Work

- **No Hook Dependency**: We don't rely on Claude Code's hook system at all
- **Full Control**: You control the launch sequence through your own alias
- **Proven Pattern**: This is how many developers launch multiple related tools
- **No Race Conditions**: Monitor launches first, returns immediately, then Claude Code launches
- **PowerShell Handles It**: PowerShell manages the wrapper script execution, not CMD hooks
