# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_handles_car_without_last_service_reading():
    fleet = [{"id": "VOS-7788", "odometer": 92000}]

    assert fleet_summary(fleet) == {
        "count": 1,
        "due": 0,
        "average_wear": 0.0,
    }
