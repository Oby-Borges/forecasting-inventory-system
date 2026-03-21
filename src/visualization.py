"""Visualization helpers for forecast comparison results."""

from __future__ import annotations

import importlib.util
import math
import struct
import zlib
from pathlib import Path

import pandas as pd


MATPLOTLIB_AVAILABLE = importlib.util.find_spec("matplotlib") is not None
if MATPLOTLIB_AVAILABLE:
    import matplotlib.pyplot as plt
else:
    plt = None

PLOT_COLUMNS = [
    "Demand",
    "Naive Forecast",
    "3-Period Moving Average",
    "Weighted Moving Average",
    "Simple Exponential Smoothing",
]

SERIES_COLORS = {
    "Demand": (31, 119, 180),
    "Naive Forecast": (255, 127, 14),
    "3-Period Moving Average": (44, 160, 44),
    "Weighted Moving Average": (214, 39, 40),
    "Simple Exponential Smoothing": (148, 103, 189),
}


def create_forecast_plot(
    forecast_data: pd.DataFrame,
    output_file: Path,
    show_plot: bool = True,
) -> None:
    """Create and save a chart that compares actual demand and forecasts."""
    required_columns = ["Period", *PLOT_COLUMNS]
    missing_columns = [column for column in required_columns if column not in forecast_data.columns]
    if missing_columns:
        missing_names = ", ".join(missing_columns)
        raise ValueError(f"Forecast plot cannot be created. Missing columns: {missing_names}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if MATPLOTLIB_AVAILABLE:
        _create_plot_with_matplotlib(forecast_data, output_file, show_plot)
    else:
        _create_plot_with_standard_library(forecast_data, output_file)



def _create_plot_with_matplotlib(
    forecast_data: pd.DataFrame,
    output_file: Path,
    show_plot: bool,
) -> None:
    """Use matplotlib when it is installed because it gives the nicest chart."""
    plt.figure(figsize=(10, 6))

    # Plot each series on the same chart so the methods are easy to compare.
    for column in PLOT_COLUMNS:
        plt.plot(
            forecast_data["Period"],
            forecast_data[column],
            marker="o",
            linewidth=2,
            label=column,
        )

    plt.title("Demand and Forecast Comparison")
    plt.xlabel("Period")
    plt.ylabel("Demand")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(output_file)

    if show_plot:
        plt.show()

    plt.close()



def _create_plot_with_standard_library(
    forecast_data: pd.DataFrame,
    output_file: Path,
) -> None:
    """Create a simple PNG chart without extra packages.

    This fallback keeps the project runnable in restricted environments where
    matplotlib cannot be installed, while still saving the requested image file.
    """
    width, height = 1200, 700
    margin_left, margin_right = 110, 40
    margin_top, margin_bottom = 70, 120

    image = _create_blank_image(width, height, background=(255, 255, 255))
    plot_left = margin_left
    plot_right = width - margin_right
    plot_top = margin_top
    plot_bottom = height - margin_bottom
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top

    periods = forecast_data["Period"].tolist()
    series_data = {column: forecast_data[column].tolist() for column in PLOT_COLUMNS}
    all_values = [
        float(value)
        for values in series_data.values()
        for value in values
        if pd.notna(value)
    ]
    min_value = min(all_values)
    max_value = max(all_values)

    if math.isclose(min_value, max_value):
        min_value -= 1
        max_value += 1

    value_padding = (max_value - min_value) * 0.1
    min_value -= value_padding
    max_value += value_padding

    _draw_rectangle_outline(image, plot_left, plot_top, plot_right, plot_bottom, (0, 0, 0))

    # Light grid lines make the chart easier to read.
    y_tick_count = 5
    for tick_index in range(y_tick_count + 1):
        y = plot_top + int(plot_height * tick_index / y_tick_count)
        _draw_line(image, plot_left, y, plot_right, y, (220, 220, 220), thickness=1)

        tick_value = max_value - ((max_value - min_value) * tick_index / y_tick_count)
        _draw_number(image, 20, y - 8, tick_value, (0, 0, 0), digits_after_decimal=1)

    if len(periods) == 1:
        x_positions = [plot_left + plot_width // 2]
    else:
        x_positions = [
            plot_left + int(plot_width * index / (len(periods) - 1))
            for index in range(len(periods))
        ]

    for x, period in zip(x_positions, periods):
        _draw_line(image, x, plot_bottom, x, plot_bottom + 8, (0, 0, 0), thickness=1)
        _draw_text(image, x - 8, plot_bottom + 18, str(period), (0, 0, 0), scale=2)

    for column, values in series_data.items():
        valid_points = []
        for x, value in zip(x_positions, values):
            if pd.isna(value):
                continue
            y_ratio = (float(value) - min_value) / (max_value - min_value)
            y = plot_bottom - int(y_ratio * plot_height)
            valid_points.append((x, y))

        if not valid_points:
            continue

        color = SERIES_COLORS[column]
        for start, end in zip(valid_points, valid_points[1:]):
            _draw_line(image, start[0], start[1], end[0], end[1], color, thickness=3)
        for x, y in valid_points:
            _draw_circle(image, x, y, radius=4, color=color)

    _draw_text(image, 360, 20, "Demand and Forecast Comparison", (0, 0, 0), scale=3)
    _draw_text(image, 520, height - 60, "Period", (0, 0, 0), scale=3)
    _draw_text(image, 20, 30, "Demand", (0, 0, 0), scale=2)
    _draw_legend(image, width - 360, height - 105)
    _write_png(output_file, image)



def _draw_legend(image: list[list[tuple[int, int, int]]], x: int, y: int) -> None:
    """Draw a small legend block that matches each series color to its label."""
    box_width = 18
    line_height = 20

    for index, column in enumerate(PLOT_COLUMNS):
        row_y = y + index * line_height
        color = SERIES_COLORS[column]
        _fill_rectangle(image, x, row_y, x + box_width, row_y + 10, color)
        _draw_text(image, x + 28, row_y - 2, column, (0, 0, 0), scale=1)



def _create_blank_image(
    width: int,
    height: int,
    background: tuple[int, int, int],
) -> list[list[tuple[int, int, int]]]:
    """Return a blank image stored as rows of RGB pixels."""
    return [[background for _ in range(width)] for _ in range(height)]



def _set_pixel(
    image: list[list[tuple[int, int, int]]],
    x: int,
    y: int,
    color: tuple[int, int, int],
) -> None:
    """Safely color a single pixel if it is inside the image bounds."""
    height = len(image)
    width = len(image[0])
    if 0 <= x < width and 0 <= y < height:
        image[y][x] = color



def _draw_line(
    image: list[list[tuple[int, int, int]]],
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: tuple[int, int, int],
    thickness: int = 1,
) -> None:
    """Draw a line using a simple step-based interpolation approach."""
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for step in range(steps + 1):
        x = round(x1 + (x2 - x1) * step / steps)
        y = round(y1 + (y2 - y1) * step / steps)
        for offset_x in range(-thickness // 2, thickness // 2 + 1):
            for offset_y in range(-thickness // 2, thickness // 2 + 1):
                _set_pixel(image, x + offset_x, y + offset_y, color)



def _draw_circle(
    image: list[list[tuple[int, int, int]]],
    center_x: int,
    center_y: int,
    radius: int,
    color: tuple[int, int, int],
) -> None:
    """Draw a filled circle to highlight each plotted point."""
    for x in range(center_x - radius, center_x + radius + 1):
        for y in range(center_y - radius, center_y + radius + 1):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius**2:
                _set_pixel(image, x, y, color)



def _draw_rectangle_outline(
    image: list[list[tuple[int, int, int]]],
    left: int,
    top: int,
    right: int,
    bottom: int,
    color: tuple[int, int, int],
) -> None:
    """Draw the outline of a rectangle."""
    _draw_line(image, left, top, right, top, color)
    _draw_line(image, left, bottom, right, bottom, color)
    _draw_line(image, left, top, left, bottom, color)
    _draw_line(image, right, top, right, bottom, color)



def _fill_rectangle(
    image: list[list[tuple[int, int, int]]],
    left: int,
    top: int,
    right: int,
    bottom: int,
    color: tuple[int, int, int],
) -> None:
    """Fill a rectangle with one color."""
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            _set_pixel(image, x, y, color)


FONT = {
    " ": ["000", "000", "000", "000", "000"],
    "-": ["000", "000", "111", "000", "000"],
    ".": ["000", "000", "000", "000", "010"],
    "0": ["111", "101", "101", "101", "111"],
    "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"],
    "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"],
    "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"],
    "9": ["111", "101", "111", "001", "111"],
    "A": ["111", "101", "111", "101", "101"],
    "C": ["111", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "G": ["111", "100", "101", "101", "111"],
    "H": ["101", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "L": ["100", "100", "100", "100", "111"],
    "M": ["101", "111", "111", "101", "101"],
    "N": ["101", "111", "111", "111", "101"],
    "O": ["111", "101", "101", "101", "111"],
    "P": ["111", "101", "111", "100", "100"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["111", "100", "111", "001", "111"],
    "T": ["111", "010", "010", "010", "010"],
    "V": ["101", "101", "101", "101", "010"],
    "W": ["101", "101", "111", "111", "101"],
    "X": ["101", "101", "010", "101", "101"],
    "a": ["000", "011", "001", "011", "011"],
    "c": ["000", "011", "100", "100", "011"],
    "d": ["001", "011", "101", "101", "011"],
    "e": ["000", "010", "111", "100", "011"],
    "g": ["000", "011", "101", "011", "001"],
    "h": ["100", "100", "110", "101", "101"],
    "i": ["010", "000", "010", "010", "010"],
    "l": ["010", "010", "010", "010", "011"],
    "m": ["000", "110", "111", "101", "101"],
    "n": ["000", "110", "101", "101", "101"],
    "o": ["000", "010", "101", "101", "010"],
    "p": ["000", "110", "101", "110", "100"],
    "r": ["000", "101", "110", "100", "100"],
    "s": ["000", "011", "110", "011", "110"],
    "t": ["010", "111", "010", "010", "011"],
    "u": ["000", "101", "101", "101", "011"],
    "v": ["000", "101", "101", "101", "010"],
    "w": ["000", "101", "111", "111", "101"],
    "x": ["000", "101", "010", "010", "101"],
}



def _draw_text(
    image: list[list[tuple[int, int, int]]],
    x: int,
    y: int,
    text: str,
    color: tuple[int, int, int],
    scale: int = 2,
) -> None:
    """Draw simple bitmap text using a tiny built-in font."""
    cursor_x = x
    for character in text:
        pattern = FONT.get(character, FONT[" "])
        for row_index, row in enumerate(pattern):
            for column_index, pixel in enumerate(row):
                if pixel == "1":
                    for scale_x in range(scale):
                        for scale_y in range(scale):
                            _set_pixel(
                                image,
                                cursor_x + column_index * scale + scale_x,
                                y + row_index * scale + scale_y,
                                color,
                            )
        cursor_x += (len(pattern[0]) + 1) * scale



def _draw_number(
    image: list[list[tuple[int, int, int]]],
    x: int,
    y: int,
    value: float,
    color: tuple[int, int, int],
    digits_after_decimal: int,
) -> None:
    """Draw a formatted number on the image."""
    formatted_value = f"{value:.{digits_after_decimal}f}"
    _draw_text(image, x, y, formatted_value, color, scale=2)



def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """Build one PNG chunk with length and CRC fields."""
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    )



def _write_png(output_file: Path, image: list[list[tuple[int, int, int]]]) -> None:
    """Write the in-memory RGB image to a PNG file."""
    height = len(image)
    width = len(image[0])

    raw_rows = []
    for row in image:
        row_bytes = bytearray([0])
        for red, green, blue in row:
            row_bytes.extend([red, green, blue])
        raw_rows.append(bytes(row_bytes))

    pixel_data = zlib.compress(b"".join(raw_rows), level=9)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

    png_bytes = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", header),
            _png_chunk(b"IDAT", pixel_data),
            _png_chunk(b"IEND", b""),
        ]
    )
    output_file.write_bytes(png_bytes)
