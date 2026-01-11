"""Tool logs panel for dedicated tool execution display."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widget import Widget

from vibe.cli.textual_ui.widgets.panels.base_panel import BasePanel


class ToolLogsPanel(BasePanel):
    """Panel for displaying tool execution logs."""

    MAX_TOOL_LOGS = 50  # Keep last 50 tool executions

    def __init__(self, **kwargs) -> None:
        super().__init__(title="Tool Logs", **kwargs)
        self._scroll_container: VerticalScroll | None = None

    def compose(self) -> ComposeResult:
        """Compose tool logs panel with scrollable container."""
        yield from super().compose()

        self._scroll_container = VerticalScroll(id="tool-logs-scroll", classes="tool-logs-container")
        yield self._scroll_container

    async def add_tool_log(self, tool_widget: Widget) -> None:
        """Add a tool execution log to the panel."""
        if not self._scroll_container:
            return

        await self._scroll_container.mount(tool_widget)

        # Cleanup old logs if exceeding limit
        children = list(self._scroll_container.children)
        if len(children) > self.MAX_TOOL_LOGS:
            oldest = children[:-self.MAX_TOOL_LOGS]
            for widget in oldest:
                await widget.remove()

        # Auto-scroll to bottom
        self.call_later(lambda: self._scroll_container.scroll_end(animate=False))

    async def clear_logs(self) -> None:
        """Clear all tool logs."""
        if self._scroll_container:
            await self._scroll_container.remove_children()
