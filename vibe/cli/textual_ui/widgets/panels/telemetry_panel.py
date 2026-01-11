"""Telemetry panel with live metrics and sparklines."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.panels.base_panel import BasePanel
from vibe.cli.textual_ui.widgets.sparkline import Sparkline

if TYPE_CHECKING:
    from vibe.core.agent import AgentStats


class TelemetryPanel(BasePanel):
    """Panel displaying live telemetry data with sparklines."""

    def __init__(self, **kwargs) -> None:
        super().__init__(title="Telemetry", **kwargs)
        self._token_sparkline: Sparkline | None = None
        self._duration_sparkline: Sparkline | None = None
        self._cost_sparkline: Sparkline | None = None
        self._stats_display: Static | None = None

    def compose(self) -> ComposeResult:
        """Compose telemetry panel with sparklines and stats."""
        yield from super().compose()

        # Token usage sparkline
        yield Static("[dim]Tokens/Turn[/dim]", classes="metric-label")
        self._token_sparkline = Sparkline(max_points=15, classes="sparkline")
        yield self._token_sparkline

        # Response duration sparkline
        yield Static("[dim]Duration (s)[/dim]", classes="metric-label")
        self._duration_sparkline = Sparkline(max_points=15, classes="sparkline")
        yield self._duration_sparkline

        # Cost sparkline
        yield Static("[dim]Cost ($)[/dim]", classes="metric-label")
        self._cost_sparkline = Sparkline(max_points=15, classes="sparkline")
        yield self._cost_sparkline

        # Summary statistics
        self._stats_display = Static("", classes="stats-summary")
        yield self._stats_display

    def update_from_stats(self, stats: AgentStats) -> None:
        """Update telemetry display with latest agent stats."""
        if not stats:
            return

        # Update sparklines
        if self._token_sparkline and hasattr(stats, 'last_turn_total_tokens'):
            self._token_sparkline.add_point(float(stats.last_turn_total_tokens))

        if self._duration_sparkline and hasattr(stats, 'last_turn_duration'):
            self._duration_sparkline.add_point(stats.last_turn_duration)

        if self._cost_sparkline and hasattr(stats, 'last_turn_cost'):
            self._cost_sparkline.add_point(stats.last_turn_cost * 1000)  # Convert to millicents for better visualization

        # Update summary stats
        if self._stats_display:
            summary_lines = []

            if hasattr(stats, 'total_tokens'):
                summary_lines.append(f"Total: {stats.total_tokens:,} tokens")

            if hasattr(stats, 'total_cost'):
                summary_lines.append(f"Cost: ${stats.total_cost:.4f}")

            if hasattr(stats, 'turns'):
                summary_lines.append(f"Turns: {stats.turns}")

            self._stats_display.update("\n".join(summary_lines))

    def clear_metrics(self) -> None:
        """Clear all metrics and sparklines."""
        if self._token_sparkline:
            self._token_sparkline.clear()
        if self._duration_sparkline:
            self._duration_sparkline.clear()
        if self._cost_sparkline:
            self._cost_sparkline.clear()
        if self._stats_display:
            self._stats_display.update("")
