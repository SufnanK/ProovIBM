# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

from pathlib import Path

SETTINGS_FILE = Path(__file__).with_name("settings.cfg")

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | Path | None = None) -> dict[str, str]:
    """Load known settings from the configuration file."""
    if path is None:
        path = SETTINGS_FILE
    settings = {}
    with open(path, encoding="utf-8") as config_file:
        for raw_line in config_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = (part.strip() for part in line.split("=", 1))
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Read an integer setting, returning a fallback when invalid or absent."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Read a string setting with a fallback."""
    return settings.get(key, fallback)
