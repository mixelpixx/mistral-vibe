"""Memory bank panel for context and memory visualization."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.widgets import ProgressBar, Static

from vibe.cli.textual_ui.widgets.panels.base_panel import BasePanel

if TYPE_CHECKING:
    from vibe.core.agent import AgentStats


class MemoryPanel(BasePanel):
    """Panel displaying context usage and memory statistics."""

    def __init__(self, max_context: int = 200_000, **kwargs) -> None:
        super().__init__(title="Memory Bank", **kwargs)
        self._max_context = max_context
        self._progress_bar: ProgressBar | None = None
        self._stats_display: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose memory panel with progress bar and stats."""
        yield from super().compose()

        # Context usage progress bar
        yield Static("[dim]Context Usage[/dim]", classes="metric-label")
        self._progress_bar = ProgressBar(total=100, show_eta=False, classes="context-progress")
        yield self._progress_bar

        # Memory statistics
        self._stats_display = Static("", classes="memory-stats")
        yield self._stats_display

    def update_from_stats(self, message_count: int, stats: AgentStats | None, max_context: int | None = None) -> None:
        """Update memory display with agent state."""
        if max_context:
            self._max_context = max_context

        # Update progress bar
        if self._progress_bar and stats and hasattr(stats, 'context_tokens'):
            context_tokens = stats.context_tokens
            percentage = min(100, (context_tokens / self._max_context) * 100) if self._max_context > 0 else 0
            self._progress_bar.update(progress=percentage)

        # Update stats
        if self._stats_display:
            lines = []

            lines.append(f"Messages: {message_count}")

            if stats:
                if hasattr(stats, 'context_tokens'):
                    lines.append(f"Tokens: {stats.context_tokens:,}/{self._max_context:,}")

                if hasattr(stats, 'turns'):
                    lines.append(f"Turns: {stats.turns}")

            self._stats_display.update("\n".join(lines))

    def set_max_context(self, max_context: int) -> None:
        """Update maximum context size."""
        self._max_context = max_context
