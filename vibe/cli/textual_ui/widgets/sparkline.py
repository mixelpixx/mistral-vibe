"""Sparkline widget for inline data visualization."""

from __future__ import annotations

from textual.reactive import reactive
from textual.widget import Widget


class Sparkline(Widget):
    """A sparkline widget for visualizing time-series data using block characters."""

    # Unicode block characters from low to high
    BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    data_points: reactive[list[float]] = reactive(list, init=False)
    max_points: reactive[int] = reactive(20)
    min_value: reactive[float | None] = reactive(None)
    max_value: reactive[float | None] = reactive(None)

    def __init__(
        self,
        initial_data: list[float] | None = None,
        max_points: int = 20,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.data_points = initial_data or []
        self.max_points = max_points

    def add_point(self, value: float) -> None:
        """Add a data point to the sparkline."""
        self.data_points = [*self.data_points, value]
        if len(self.data_points) > self.max_points:
            self.data_points = self.data_points[-self.max_points:]
        self.refresh()

    def set_data(self, data: list[float]) -> None:
        """Set all data points at once."""
        self.data_points = data[-self.max_points:] if len(data) > self.max_points else list(data)
        self.refresh()

    def clear(self) -> None:
        """Clear all data points."""
        self.data_points = []
        self.refresh()

    def _normalize_value(self, value: float, min_val: float, max_val: float) -> int:
        """Normalize a value to a block index (0-7)."""
        if max_val == min_val:
            return len(self.BLOCKS) // 2

        normalized = (value - min_val) / (max_val - min_val)
        index = int(normalized * (len(self.BLOCKS) - 1))
        return max(0, min(len(self.BLOCKS) - 1, index))

    def render(self) -> str:
        """Render the sparkline as a string of block characters."""
        if not self.data_points:
            return "─" * self.max_points

        # Determine min/max values
        min_val = self.min_value if self.min_value is not None else min(self.data_points)
        max_val = self.max_value if self.max_value is not None else max(self.data_points)

        # Generate sparkline
        blocks = []
        for value in self.data_points:
            block_index = self._normalize_value(value, min_val, max_val)
            blocks.append(self.BLOCKS[block_index])

        # Pad with spaces if needed
        while len(blocks) < self.max_points:
            blocks.insert(0, " ")

        return "".join(blocks)
