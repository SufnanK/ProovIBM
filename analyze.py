# Breakdown risk is driven most by km since service, followed by daily use and load factor.
# Odometer mileage and vehicle age do not separate breakdowns; their group averages are almost identical.

"""Compare breakdown groups and rank the fleet with a simple risk score."""

from pathlib import Path

import numpy as np
import pandas as pd

HISTORY_FILE = Path(__file__).with_name("fleet_history.csv")
OUTCOME = "broke_down"
PERMUTATIONS = 20_000
RANDOM_SEED = 42


def standardized_mean_difference(
    broke_down: pd.Series, did_not_break_down: pd.Series
) -> float:
    """Return the group mean difference measured in pooled standard deviations."""
    numerator = broke_down.mean() - did_not_break_down.mean()
    pooled_variance = (
        (len(broke_down) - 1) * broke_down.var()
        + (len(did_not_break_down) - 1) * did_not_break_down.var()
    ) / (len(broke_down) + len(did_not_break_down) - 2)
    return numerator / np.sqrt(pooled_variance)


def permutation_p_value(
    values: pd.Series, outcomes: pd.Series, observed_difference: float
) -> float:
    """Estimate a two-sided p-value by repeatedly shuffling breakdown labels."""
    rng = np.random.default_rng(RANDOM_SEED)
    values_array = values.to_numpy()
    outcomes_array = outcomes.to_numpy(dtype=bool)
    equally_extreme = 0

    for _ in range(PERMUTATIONS):
        shuffled = rng.permutation(outcomes_array)
        difference = (
            values_array[shuffled].mean() - values_array[~shuffled].mean()
        )
        equally_extreme += abs(difference) >= abs(observed_difference)

    return (equally_extreme + 1) / (PERMUTATIONS + 1)


def compare_groups(data: pd.DataFrame) -> pd.DataFrame:
    """Compare every candidate numeric feature between outcome groups."""
    features = data.select_dtypes(include="number").columns.drop(OUTCOME)
    rows = []

    for feature in features:
        broke_down = data.loc[data[OUTCOME] == 1, feature]
        did_not_break_down = data.loc[data[OUTCOME] == 0, feature]
        mean_difference = broke_down.mean() - did_not_break_down.mean()
        effect_size = standardized_mean_difference(
            broke_down, did_not_break_down
        )
        p_value = permutation_p_value(
            data[feature], data[OUTCOME], mean_difference
        )
        rows.append(
            {
                "feature": feature,
                "no_breakdown_mean": did_not_break_down.mean(),
                "breakdown_mean": broke_down.mean(),
                "mean_difference": mean_difference,
                "effect_size": effect_size,
                "p_value": p_value,
                "separates_groups": (
                    abs(effect_size) >= 0.5 and p_value < 0.05
                ),
            }
        )

    return pd.DataFrame(rows).set_index("feature")


def add_risk_score(
    data: pd.DataFrame, comparisons: pd.DataFrame
) -> tuple[pd.DataFrame, pd.Series]:
    """Add a 0–100 score using only features that clearly separate the groups."""
    selected = comparisons.index[comparisons["separates_groups"]]
    weights = comparisons.loc[selected, "effect_size"].abs()
    weights /= weights.sum()

    scaled = data[selected].apply(
        lambda column: (
            (column - column.min()) / (column.max() - column.min())
        )
    )
    raw_score = scaled.mul(weights).sum(axis=1)
    score = (
        100
        * (raw_score - raw_score.min())
        / (raw_score.max() - raw_score.min())
    )

    ranked = data.copy()
    ranked["risk_score"] = score.round(1)
    ranked = ranked.sort_values("risk_score", ascending=False)
    return ranked, weights


def main() -> None:
    """Load history, explain feature separation, and print the ten riskiest cars."""
    fleet = pd.read_csv(HISTORY_FILE)
    comparisons = compare_groups(fleet)
    ranked, weights = add_risk_score(fleet, comparisons)

    print(f"Loaded {len(fleet)} cars from {HISTORY_FILE.name}.")
    print(
        f"Breakdowns: {fleet[OUTCOME].sum()}; "
        f"no breakdown: {(fleet[OUTCOME] == 0).sum()}\n"
    )
    print(
        "Group comparison "
        "(effect size is the standardized mean difference):"
    )
    print(comparisons.round(3).to_string())
    print("\nSelected risk factors and weights:")
    print((weights * 100).round(1).rename("weight_percent").to_string())
    print("\nTop 10 cars by risk:")
    columns = ["car_id", *weights.index, "risk_score"]
    print(ranked.loc[:, columns].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
