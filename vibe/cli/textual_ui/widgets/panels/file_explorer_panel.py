"""File explorer panel for tracking recent file operations."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.panels.base_panel import BasePanel


class FileExplorerPanel(BasePanel):
    """Panel displaying recently accessed files."""

    MAX_RECENT_FILES = 10

    def __init__(self, **kwargs) -> None:
        super().__init__(title="File Explorer", **kwargs)
        self._recent_files: deque[str] = deque(maxlen=self.MAX_RECENT_FILES)
        self._files_display: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose file explorer panel."""
        yield from super().compose()

        yield Static("[dim]Recent Files[/dim]", classes="section-label")
        self._files_display = Static(self._format_files(), classes="files-list")
        yield self._files_display

    def add_file(self, file_path: Path | str) -> None:
        """Track a recently accessed file."""
        path_str = str(file_path)

        # Remove if already exists (to move to front)
        if path_str in self._recent_files:
            self._recent_files.remove(path_str)

        self._recent_files.appendleft(path_str)
        self._update_display()

    def _format_files(self) -> str:
        """Format recent files for display."""
        if not self._recent_files:
            return "[dim]No recent files[/dim]"

        lines = []
        for i, file_path in enumerate(self._recent_files, 1):
            # Show just the filename, with relative path on hover
            path = Path(file_path)
            filename = path.name
            lines.append(f"{i:2d}. {filename}")

        return "\n".join(lines)

    def _update_display(self) -> None:
        """Update the files display."""
        if self._files_display:
            self._files_display.update(self._format_files())

    def clear_files(self) -> None:
        """Clear recent files list."""
        self._recent_files.clear()
        self._update_display()
