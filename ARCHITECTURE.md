# Architecture Documentation

## System Overview

The Claude Code Odometer Monitor is a lightweight desktop widget that provides real-time token usage monitoring for Claude Code sessions.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                           ↓                                 │
│                     Interacts with                          │
│                           ↓                                 │
├─────────────────────────────────────────────────────────────┤
│                    UI LAYER (tkinter)                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  ui_widget.py - OdometerWidget                        │ │
│  │  - Percentage display (color-coded)                   │ │
│  │  - Progress bar (Canvas)                              │ │
│  │  - Token count label                                  │ │
│  │  - Plan label                                         │ │
│  │  - Compress button                                    │ │
│  │  - Draggable window                                   │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                 │
├─────────────────────────────────────────────────────────────┤
│                   BUSINESS LOGIC LAYER                      │
│  ┌──────────────────┐  ┌───────────────────────────────┐  │
│  │ token_calculator │  │  compress_handler             │  │
│  │ - calculate_%    │  │  - copy_to_clipboard()        │  │
│  │ - get_color()    │  │  - execute_compress()         │  │
│  │ - should_enable()│  │  - show_notification()        │  │
│  └──────────────────┘  └───────────────────────────────┘  │
│                           ↓                                 │
├─────────────────────────────────────────────────────────────┤
│                     DATA LAYER                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  data_reader.py                                       │ │
│  │  - find_active_session()                              │ │
│  │  - read_session_tokens()                              │ │
│  │  - extract_tokens_from_entry()                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                           ↓                                 │
├─────────────────────────────────────────────────────────────┤
│                  FILE SYSTEM LAYER                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  ~/.claude/projects/**/*.jsonl                        │ │
│  │  - Claude Code session logs                           │ │
│  │  - Token usage data                                   │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  ~/.claude-monitor/position.json                      │ │
│  │  - Window position persistence                        │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Entry Point
**main.py**
- Creates tkinter root window
- Initializes OdometerWidget
- Sets up compress handler callback
- Manages window position loading/saving
- Orchestrates 2-second polling loop
- Handles application lifecycle

### Configuration
**config.py**
- Defines plan limits (Pro, Max5, Max20)
- Sets refresh interval
- Configures Claude directories
- Defines window dimensions
- Specifies color thresholds
- Sets compress threshold
- Defines persistence paths

### Data Access Layer
**data_reader.py**
- `find_active_session()`: Locates most recent JSONL file
- `read_session_tokens()`: Parses entire JSONL file
- `extract_tokens_from_entry()`: Sums tokens from single entry
- `get_current_usage()`: Convenience function for current state

### Business Logic Layer
**token_calculator.py**
- `calculate_usage()`: Computes percentage from raw tokens
- `get_color_for_percentage()`: Maps percentage to color code
- `should_enable_compress()`: Determines button state
- `get_usage_data()`: Returns complete display data dictionary

**compress_handler.py**
- `copy_to_clipboard()`: Copies text to system clipboard
- `execute_compress()`: Orchestrates compress command flow
- `create_compress_handler()`: Factory function

### UI Layer
**ui_widget.py**
- Creates and manages all UI elements
- Implements draggable window behavior
- Updates display with current usage data
- Handles compress button clicks
- Shows "No active session" state
- Manages progress bar rendering

## Data Flow

### Polling Cycle (Every 2 Seconds)
```
1. Timer triggers refresh()
   ↓
2. OdometerWidget.update_display() called
   ↓
3. data_reader.get_current_usage()
   ├─→ find_active_session() → most recent JSONL path
   └─→ read_session_tokens() → total token count
       └─→ extract_tokens_from_entry() (for each line)
           └─→ sum all token types
   ↓
4. token_calculator.get_usage_data()
   ├─→ calculate_usage() → percentage
   ├─→ get_color_for_percentage() → color code
   └─→ should_enable_compress() → button state
   ↓
5. UI updates:
   ├─→ percentage_label.config(text, fg)
   ├─→ progress_canvas.coords() and itemconfig()
   ├─→ token_label.config(text)
   └─→ compress_button.config(state, bg, fg)
   ↓
6. Schedule next refresh in 2 seconds
```

### Compress Button Click Flow
```
1. User clicks compress button
   ↓
2. OdometerWidget._on_compress_click()
   ↓
3. compress_callback() invoked
   ↓
4. CompressHandler.execute_compress()
   ├─→ copy_to_clipboard("/compress")
   └─→ messagebox.showinfo() with instructions
   ↓
5. User pastes into Claude Code terminal
```

### Window Position Persistence Flow
```
STARTUP:
1. main() creates root window
   ↓
2. load_window_position()
   ├─→ Read ~/.claude-monitor/position.json
   ├─→ Validate position is on-screen
   └─→ Apply geometry or center if invalid
   ↓
3. Window appears at saved/centered position

SHUTDOWN:
1. User closes window
   ↓
2. WM_DELETE_WINDOW protocol triggers
   ↓
3. save_and_quit()
   ├─→ save_window_position()
   │   ├─→ Get current x, y coordinates
   │   └─→ Write to position.json
   └─→ root.quit()
```

## Token Extraction Logic

### Token Types Summed
```python
total_tokens = (
    input_tokens +              # User prompts and context
    output_tokens +             # Assistant responses
    cache_read_input_tokens +   # Cache hits
    ephemeral_5m_input_tokens   # Cache creation
)
```

### Entry Filtering
- Only `"type": "assistant"` entries are counted
- User entries are ignored (they don't have usage data)
- System entries are ignored
- Invalid JSON lines are skipped gracefully

## Error Handling Strategy

### No Active Session
```
Condition: No JSONL files found or directory doesn't exist
Behavior: Display "No active session" with gray color
Recovery: Continue polling, auto-detect when session starts
```

### File Permission Errors
```
Condition: Cannot read ~/.claude/projects/ or JSONL files
Behavior: Silently return 0 tokens, show "No active session"
Recovery: Continue polling, retry on next cycle
```

### Corrupted JSONL
```
Condition: Invalid JSON line in JSONL file
Behavior: Skip line, continue processing remaining lines
Recovery: Partial token count from valid lines
```

### Window Off-Screen
```
Condition: Saved position outside current screen bounds
Behavior: Ignore saved position, center window
Recovery: New position saved on next close
```

### Missing Config Directory
```
Condition: ~/.claude-monitor/ doesn't exist
Behavior: Create directory on first position save
Recovery: Automatic directory creation
```

## Performance Optimizations

### Minimizing File I/O
- Poll every 2 seconds (not continuously)
- Read only most recent JSONL file
- Use file modification time for quick selection
- No file watching (polling is sufficient)

### UI Efficiency
- Update only changed elements
- Use Canvas for progress bar (not images)
- Minimize redraws by batching updates
- No animations (reduces CPU usage)

### Memory Management
- No session history stored in memory
- Parse JSONL line-by-line (streaming)
- No caching of old data
- Minimal state retention

## Thread Safety

### Single-Threaded Design
- All operations run on main tkinter thread
- No threading or multiprocessing used
- Polling via `root.after()` (event loop)
- No race conditions possible

## Security Considerations

### Data Access
- Read-only access to Claude Code logs
- No network access
- No external process execution
- Clipboard access for compress command only

### File System Access
```
READ:  ~/.claude/projects/**/*.jsonl
READ:  ~/.claude-monitor/position.json
WRITE: ~/.claude-monitor/position.json
```

### No Sensitive Data
- No API keys stored or accessed
- No user credentials
- No conversation content processed
- Only token counts extracted

## Extensibility Points

### Adding New Plan Types
```python
# In config.py
class PlanLimits:
    CUSTOM = 100000  # Add new plan

# In config.py
PLAN_LIMIT = PlanLimits.CUSTOM
PLAN_NAME = "Custom"
```

### Custom Color Schemes
```python
# In token_calculator.py
def get_color_for_percentage(self, pct: float) -> str:
    # Modify threshold logic
    if pct < 60:
        return Config.COLOR_SAFE
    # ... custom thresholds
```

### Additional UI Elements
```python
# In ui_widget.py
def _create_widgets(self):
    # Add new labels, buttons, or displays
    self.new_label = tk.Label(...)
    self.new_label.pack()
```

### Alternative Compress Methods
```python
# In compress_handler.py
class AdvancedCompressHandler(CompressHandler):
    def execute_compress(self):
        # Implement keyboard automation
        # Or terminal API integration
        pass
```

## Dependencies

### Core Dependencies (Built-in)
- `tkinter`: UI framework
- `json`: JSONL parsing and config storage
- `pathlib`: File system operations
- `typing`: Type hints

### No External Dependencies
- No pip packages required
- Pure Python standard library
- Cross-platform compatible
- Zero dependency management needed

## Testing Strategy

### Unit Tests
- `test_token_calculator.py`: Business logic validation
- `test_data_reader.py`: Token extraction validation

### Integration Points
- File system reads (mocked in tests)
- UI updates (manual testing)
- Window management (manual testing)

### Manual Testing Checklist
See CHANGELOG.md for complete testing checklist

## Deployment

### Distribution
- Source code distribution (no compilation)
- Single directory structure
- No build process required
- No installation script needed

### User Setup
1. Download/clone repository
2. Verify Python 3.8+ installed
3. Run `python src/main.py`
4. Window appears and begins monitoring

## Future Architecture Considerations

### For Multi-Session Support
- Add session selector dropdown
- Maintain dictionary of {session_id: usage_data}
- Switch between sessions without restart

### For Auto-Compress
- Add background thread for compress execution
- Implement terminal automation (pyautogui)
- Add confirmation dialog before auto-compress

### For System Tray Mode
- Detect system tray capability (pystray library)
- Add minimize-to-tray functionality
- Show icon with tooltip percentage

### For Usage History
- Add SQLite database for history tracking
- Store hourly/daily usage snapshots
- Generate usage trend graphs
