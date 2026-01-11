"""Layout selection screen for choosing between traditional and grid layouts."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Static


class LayoutSelectionScreen(ModalScreen[tuple[bool, bool]]):
    """Modal screen for selecting layout preference.
    
    Returns:
        Tuple of (use_grid_layout: bool, remember_choice: bool)
    """

    CSS = """
    LayoutSelectionScreen {
        align: center middle;
    }
    
    #layout-selection-container {
        width: 70;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 2;
    }
    
    #layout-title {
        width: 100%;
        text-align: center;
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }
    
    #layout-subtitle {
        width: 100%;
        text-align: center;
        color: $text;
        margin-bottom: 2;
    }
    
    .layout-option {
        width: 100%;
        height: auto;
        border: round $accent;
        padding: 1 2;
        margin-bottom: 1;
        background: $background;
    }
    
    .layout-option:hover {
        border: round $primary;
        background: $boost;
    }
    
    .layout-option-title {
        color: $primary;
        text-style: bold;
    }
    
    .layout-option-desc {
        color: $text-muted;
    }
    
    #remember-checkbox-container {
        width: 100%;
        margin-top: 1;
        margin-bottom: 2;
    }
    
    #button-container {
        width: 100%;
        height: auto;
    }
    
    .layout-button {
        margin: 0 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._selected_layout: bool = False  # False = traditional, True = grid
        self._remember_choice: bool = True  # Default to remember

    def compose(self) -> ComposeResult:
        with Vertical(id="layout-selection-container"):
            yield Static("Welcome to Mistral Vibe", id="layout-title")
            yield Static("Choose your preferred interface layout:", id="layout-subtitle")

            # Traditional layout option
            with Vertical(classes="layout-option", id="traditional-option"):
                yield Static("[bold]Traditional Layout[/bold]", classes="layout-option-title")
                yield Static(
                    "Single-column chat interface\n"
                    "Familiar, simple, and fast\n"
                    "Perfect for focused conversations",
                    classes="layout-option-desc"
                )

            # Grid layout option
            with Vertical(classes="layout-option", id="grid-option"):
                yield Static("[bold]Grid Layout (Cockpit)[/bold]", classes="layout-option-title")
                yield Static(
                    "Multi-panel interface with live metrics\n"
                    "File explorer, telemetry, memory visualization\n"
                    "Premium AI cockpit experience",
                    classes="layout-option-desc"
                )

            # Remember choice checkbox
            with Center(id="remember-checkbox-container"):
                yield Checkbox("Remember my choice", value=True, id="remember-checkbox")

            # Buttons
            with Center(id="button-container"):
                with Horizontal():
                    yield Button("Traditional", variant="primary", classes="layout-button", id="traditional-btn")
                    yield Button("Grid Layout", variant="default", classes="layout-button", id="grid-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "traditional-btn":
            self._selected_layout = False
            self._submit_choice()
        elif event.button.id == "grid-btn":
            self._selected_layout = True
            self._submit_choice()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox change."""
        if event.checkbox.id == "remember-checkbox":
            self._remember_choice = event.value

    def _submit_choice(self) -> None:
        """Submit the layout choice."""
        self.dismiss((self._selected_layout, self._remember_choice))
