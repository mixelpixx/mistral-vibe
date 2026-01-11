# Layout Selection Feature

## Overview

Mistral Vibe now features an interactive layout selection screen that appears on first run, allowing users to choose between Traditional and Grid layouts with an option to remember their preference.

## User Experience

### First Run

When you run Mistral Vibe for the first time (or if you haven't set a layout preference), you'll see a welcome screen with two layout options:

```
┌─────────────────────────────────────────────────────────────┐
│                  Welcome to Mistral Vibe                    │
│           Choose your preferred interface layout:           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Traditional Layout                                     │ │
│  │ Single-column chat interface                          │ │
│  │ Familiar, simple, and fast                            │ │
│  │ Perfect for focused conversations                     │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Grid Layout (Cockpit)                                 │ │
│  │ Multi-panel interface with live metrics              │ │
│  │ File explorer, telemetry, memory visualization       │ │
│  │ Premium AI cockpit experience                        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [✓] Remember my choice                                    │
│                                                             │
│          [Traditional]        [Grid Layout]                │
└─────────────────────────────────────────────────────────────┘
```

### Layout Options

**Traditional Layout**
- Single-column chat interface
- Familiar, simple, and fast
- Perfect for focused conversations
- Minimal resource usage
- Default behavior unchanged

**Grid Layout (Cockpit)**
- Multi-panel interface with dedicated zones
- Live telemetry with sparklines
- File explorer panel
- Tool logs panel
- Memory/context visualization
- Premium AI cockpit experience

### Remember Choice

**Checked (Default)**
- Your selection is saved to `~/.vibe/config.toml`
- The layout preference is applied on every startup
- You won't see this screen again

**Unchecked**
- Selection applies to current session only
- You'll see this screen again on next startup
- Useful for trying different layouts

## Behavior

### Selecting Traditional Layout

If you select Traditional and check "Remember my choice":
- Preference saved to config
- App continues with traditional layout
- No restart needed

### Selecting Grid Layout

If you select Grid Layout and check "Remember my choice":
- Preference saved to config
- App shows notification: "Grid layout preference saved. Please restart Vibe to apply."
- App exits after 2 seconds
- Restart Vibe to see grid layout

If you select Grid Layout and DON'T check "Remember my choice":
- Warning shown: "Grid layout requires restart. Please select 'Remember my choice' to enable."
- App continues with traditional layout for this session
- You'll see the selection screen again on next startup

## Configuration

The layout preference is stored in your `~/.vibe/config.toml`:

```toml
# Grid Layout (Bento Cockpit)
use_grid_layout = true  # or false
layout_preference_set = true
```

### Manually Changing Layout

You can change your layout preference at any time by editing the config file:

```bash
# Enable grid layout
echo 'use_grid_layout = true' >> ~/.vibe/config.toml

# Disable grid layout
sed -i 's/use_grid_layout = true/use_grid_layout = false/' ~/.vibe/config.toml
```

### Resetting Preference

To see the selection screen again:

```bash
# Remove the preference flag from config
sed -i '/layout_preference_set = true/d' ~/.vibe/config.toml
```

## Testing

### Test the Layout Selection Screen

Run the standalone test:

```bash
uv run python /tmp/test_layout_selection.py
```

Controls:
- Select Traditional or Grid Layout buttons
- Toggle "Remember my choice" checkbox with Space or click
- Press 's' to show selection screen again
- Press 'q' to quit

### Test with Vibe

1. Reset your preference (if you've already set one):
```bash
sed -i '/layout_preference_set = true/d' ~/.vibe/config.toml
```

2. Run Vibe:
```bash
uv run vibe
```

3. The layout selection screen will appear
4. Make your choice and test both layouts

## Implementation Details

### Files Added

- `vibe/cli/textual_ui/screens/layout_selection.py` - Layout selection modal screen
- `vibe/cli/textual_ui/screens/__init__.py` - Screens package initialization
- `LAYOUT_SELECTION.md` - This documentation

### Files Modified

- `vibe/core/config.py` - Added `layout_preference_set` field
- `vibe/cli/textual_ui/app.py` - Added layout selection logic in `on_mount()`

### Configuration Fields

```python
layout_preference_set: bool = Field(
    default=False,
    description="Whether user has been asked about layout preference (internal flag)"
)
```

### User Flow

```
App Start
    ↓
Check layout_preference_set
    ↓
    No → Show Layout Selection Screen
          ↓
          User selects layout + remember option
          ↓
          Remember checked?
              Yes → Save to config
                    ↓
                    Grid selected?
                        Yes → Save, notify, exit (restart needed)
                        No  → Save, continue with traditional
              No  → Continue with traditional for session
    ↓
    Yes → Use saved preference (use_grid_layout)
          ↓
          Continue with selected layout
```

## Backward Compatibility

This feature is fully backward compatible:
- Existing users with `use_grid_layout` already set won't see the selection screen
- Default behavior remains traditional layout
- No breaking changes to configuration
- Users can opt in or out at any time

## Future Enhancements

Potential improvements for this feature:

1. **In-App Layout Switching**: Add a command or keybinding to switch layouts without restart
2. **Layout Previews**: Show visual previews of each layout option
3. **Guided Tour**: After selecting grid layout, show a brief tour of panels
4. **More Layouts**: Add additional layout options (e.g., compact, widescreen)
5. **Per-Project Preferences**: Allow different layouts for different projects

---

**Status**: Production Ready ✅
**Version**: Fork exclusive feature
**Date**: 2026-01-10
