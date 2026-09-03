# log_util.py
# Eigener Logger. Das logging-Modul war uns 2013 "zu viel Magie".
# (A homemade logger. The logging module felt like "too much magic" in 2013.)

import time

LOG_LINES = []  # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Print a timestamped message and buffer it for the log file."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a debug message when debug logging is enabled."""
    # DEBUG ist seit 2014 False. Dieser Zweig ist tot. (DEBUG has been False since 2014.)
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Append buffered messages to disk, then clear the buffer."""
    with open(path, "a", encoding="utf-8") as log_file:
        for line in LOG_LINES:
            log_file.write(f"{line}\n")
    LOG_LINES.clear()
