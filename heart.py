"""Render a heart shape as ASCII art in the terminal.

This module provides a ``generate_heart`` helper that builds the
heart by sampling the implicit cardioid equation
``(x^2 + y^2 - 1)^3 - x^2 y^3 <= 0`` across a configurable grid.
The main routine exposes a small CLI so the output character and
resolution can be customised.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class HeartConfig:
    """Configuration for the ASCII heart rendering."""

    width: int = 40
    char: str = "♥"

    def __post_init__(self) -> None:
        if self.width < 10:
            raise ValueError("width must be at least 10 to render a recognisable heart")
        if len(self.char) != 1:
            raise ValueError("char must be a single character")


def generate_heart(config: HeartConfig) -> str:
    """Generate a heart shape using ASCII characters.

    Args:
        config: Rendering parameters.

    Returns:
        A multiline string that visually resembles a heart.
    """

    height = config.width // 2
    rows: list[str] = []

    x_scale = 2.0 / config.width
    y_scale = 2.0 / height if height else 0

    for y in range(height, -height - 1, -1):
        row_chars: list[str] = []
        for x in range(-config.width, config.width + 1):
            x_norm = x * x_scale
            y_norm = y * y_scale
            value = (x_norm**2 + y_norm**2 - 1) ** 3 - x_norm**2 * y_norm**3
            row_chars.append(config.char if value <= 0 else " ")
        rows.append("".join(row_chars).rstrip())

    return "\n".join(rows).rstrip()


def parse_args() -> HeartConfig:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=HeartConfig.width,
        help="overall width of the heart in characters (default: %(default)s)",
    )
    parser.add_argument(
        "-c",
        "--char",
        type=str,
        default=HeartConfig.char,
        help="single character used to draw the heart (default: '%(default)s')",
    )
    args = parser.parse_args()
    return HeartConfig(width=args.width, char=args.char)


def main() -> None:
    config = parse_args()
    print(generate_heart(config))


if __name__ == "__main__":
    main()
