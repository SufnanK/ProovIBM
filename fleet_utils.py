# fleet_utils.py
# Sammelbecken fuer Helfer seit 2013. Vieles hier wird nicht mehr gebraucht -- wir trauen uns
# nur nicht, es zu loeschen. (Catch-all helpers since 2013. Much of this is unused -- we just
# never dared to delete anything.)

from datetime import datetime
from statistics import mean as statistics_mean
from typing import TypeVar

MILES_PER_KM = 0.621371
T = TypeVar("T")


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number with one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a percentage as a whole number."""
    return f"{value:.0f}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean, or zero for an empty list."""
    return statistics_mean(values) if values else 0.0


def is_due(pct: float, threshold: float) -> bool:
    """Return whether wear has reached its warning threshold."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse a DD.MM.YYYY service date, returning None when invalid."""
    try:
        parsed = datetime.strptime(text, "%d.%m.%Y")
    except ValueError:
        return None
    return parsed.year, parsed.month, parsed.day


def chunk_list(items: list[T], size: int) -> list[list[T]]:
    """Split a list into chunks of a positive size."""
    if size <= 0:
        raise ValueError("chunk size must be positive")
    return [items[index:index + size] for index in range(0, len(items), size)]
