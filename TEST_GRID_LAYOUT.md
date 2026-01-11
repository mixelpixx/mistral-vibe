# Testing the Grid Layout / UX Overhaul

## Quick Test

### 1. Enable Grid Layout

Edit your config file:
```bash
echo 'use_grid_layout = true' >> ~/.vibe/config.toml
```

### 2. Run Vibe

```bash
uv run vibe
```

You should see the new grid layout with 5 panels:
- File Explorer (left)
- Main Chat (center)
- Telemetry (right top)
- Tool Logs (left bottom)
- Memory Bank (right bottom)

### 3. Test Features

**Panel Toggles:**
- `Ctrl+1` - Toggle File Explorer
- `Ctrl+2` - Toggle Telemetry
- `Ctrl+3` - Toggle Tool Logs
- `Ctrl+4` - Toggle Memory Bank

**Interact with the agent:**
- Ask it to read/write files - File Explorer will update
- Run any command - Telemetry sparklines will show metrics
- Watch the chat panel border pulse while the agent thinks
- Memory panel shows context usage and message count

### 4. Reset to Linear Mode

```bash
sed -i '/use_grid_layout = true/d' ~/.vibe/config.toml
uv run vibe
```

The traditional linear layout will be back.

## Standalone Test (Optional)

To test just the grid layout without the full agent:

```bash
uv run python /tmp/test_full_ux.py
```

**Test Controls:**
- `Ctrl+1-4`: Toggle panels
- `t`: Toggle thinking animation
- `u`: Update metrics with test data
- `q`: Quit

This will show all panels with sample data and let you test the UI features.

## Features to Test

1. **Grid Layout**
   - All 5 panels visible
   - Proper spacing and borders
   - Responsive to terminal resize

2. **Sparklines** (Telemetry Panel)
   - Token usage per turn
   - Response duration
   - Cost tracking
   - Updates after each agent turn

3. **File Tracking** (File Explorer)
   - Shows recently accessed files
   - Updates when Read/Write/Edit tools used

4. **Memory Visualization** (Memory Panel)
   - Progress bar for context usage
   - Message and turn counters
   - Token statistics

5. **Thinking Animation**
   - Chat panel border pulses while agent works
   - Returns to normal when complete

6. **Panel Controls**
   - Toggle any panel with Ctrl+1-4
   - Panels hide/show smoothly

## Verify Backward Compatibility

1. Disable grid layout (remove from config or set to false)
2. Run vibe - should work exactly as before
3. All features functional in linear mode
4. No performance impact

## Expected Behavior

**Grid Mode:**
- Multi-panel layout
- Live metrics in telemetry panel
- File tracking in explorer panel
- Context visualization in memory panel
- Thinking animations

**Linear Mode (Default):**
- Traditional single-column chat
- All existing functionality intact
- No visual changes
- Zero overhead

## Troubleshooting

**Grid not showing:**
- Check `use_grid_layout = true` in `~/.vibe/config.toml`
- Restart vibe after config change

**Panels not updating:**
- Interact with the agent (send a message)
- Panels update after each turn completes

**Missing sparklines:**
- Only visible in grid mode
- Need at least one agent interaction to show data
