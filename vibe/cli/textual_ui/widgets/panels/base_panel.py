"""Base panel class for Bento Grid panels."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Static


class BasePanel(Vertical):
    """Base class for all Bento Grid panels."""

    visible: reactive[bool] = reactive(True)

    def __init__(
        self,
        title: str = "",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._title = title
        self._title_widget: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose the panel with title."""
        if self._title:
            self._title_widget = Static(f"[bold]{self._title}[/bold]", classes="panel-title")
            yield self._title_widget

    def set_title(self, title: str) -> None:
        """Update panel title."""
        self._title = title
        if self._title_widget:
            self._title_widget.update(f"[bold]{title}[/bold]")

    def watch_visible(self, visible: bool) -> None:
        """React to visibility changes."""
        self.display = visible

    def hide(self) -> None:
        """Hide the panel."""
        self.visible = False

    def show(self) -> None:
        """Show the panel."""
        self.visible = True

    def toggle_visibility(self) -> None:
        """Toggle panel visibility."""
        self.visible = not self.visible
