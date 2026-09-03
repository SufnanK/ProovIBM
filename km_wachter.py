# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Nobody has cleaned it up since.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: int, interval: int) -> float:
    """Return the percentage of a service interval already driven."""
    ratio = km_since_service / interval
    return ratio * 100


def needs_service(car: dict[str, object]) -> bool:
    """Return whether a car with a known service reading is due soon."""
    last = car.get("last_service_km")
    if last is None:
        return False

    km_since = car["odometer"] - last
    pct = wear_percent(km_since, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict[str, object]]) -> list[str]:
    """Print and return the IDs of cars that need service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
