"""
Assumption_DB loader + lookup for Dash ROI v3.
Replaces the v2 4-criteria INDEX/MATCH with a pandas filter.

Reads Assumption.csv (exported from Pro v2's Assumption_DB sheet),
cleans the export quirks, and returns the assumption set for a given
(State, PropertyType, ModelType, Scenario) combination.

All percentage columns are returned as DECIMALS (6.00% -> 0.06),
matching the engine convention. Dollar columns are plain floats.
"""

import pandas as pd
from pathlib import Path

# CSV lives in the project root, one level up from this engine/ folder.
CSV_PATH = Path(__file__).resolve().parent.parent / "Assumption.csv"

# Columns that come in as "6.00%" text and must become decimals.
PERCENT_COLS = [
    "RentGrowth Annual", "Inflation Annual", "Appreciation Annual",
    "Management Fee", "Closing Cost Buying", "PropertyTaxRate Annual",
    "VacancyRate% Annual", "Maintenance% Annual", "CapEx% Annual",
    "SellingCost% Annual", "Tax Growth",
]
# Columns that come in as "$1,900.00" or "$200.00" and must become floats.
DOLLAR_COLS = ["Insurance Yearly", "HOA Monthly"]

# The four lookup keys.
KEY_COLS = ["State", "PropertyType", "ModelType", "Scenario"]


def _clean_percent(series):
    """'6.00%' -> 0.06 . Strip the % sign and divide by 100."""
    return series.astype(str).str.replace("%", "", regex=False).astype(float) / 100


def _clean_dollar(series):
    """'$1,900.00' -> 1900.0 . Strip $ and thousands commas."""
    return (series.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float))


def load_assumptions(csv_path=CSV_PATH):
    """Load and clean the assumption table. Returns a pandas DataFrame."""
    # utf-8-sig strips the BOM so the first column is 'State', not '\ufeffState'.
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # Drop the empty spacer rows (all-key-columns blank).
    df = df.dropna(subset=KEY_COLS).reset_index(drop=True)

    # Trim stray whitespace on the text keys so lookups match cleanly.
    for col in KEY_COLS:
        df[col] = df[col].astype(str).str.strip()

    # Convert the % columns present in the file to decimals.
    for col in PERCENT_COLS:
        if col in df.columns:
            df[col] = _clean_percent(df[col])

    # Convert the $ columns to floats.
    for col in DOLLAR_COLS:
        if col in df.columns:
            df[col] = _clean_dollar(df[col])

    return df


def get_assumptions(state, property_type, model, scenario, df=None):
    """
    Return the single assumption row matching the four keys, as a dict.
    This is the pandas equivalent of the v2 INDEX/MATCH.
    Raises if no row (or more than one) matches.
    """
    if df is None:
        df = load_assumptions()

    match = df[
        (df["State"] == state)
        & (df["PropertyType"] == property_type)
        & (df["ModelType"] == model)
        & (df["Scenario"] == scenario)
    ]

    if len(match) == 0:
        raise ValueError(
            f"No assumption row for {state}/{property_type}/{model}/{scenario}"
        )
    if len(match) > 1:
        raise ValueError(
            f"Multiple rows for {state}/{property_type}/{model}/{scenario}"
        )

    return match.iloc[0].to_dict()


# --- Validation against the Week-4 reference row ---
if __name__ == "__main__":
    row = get_assumptions("Illinois", "Townhouse", "Rental", "Conservative")

    print("Illinois / Townhouse / Rental / Conservative:")
    print(f"  Vacancy:      {row['VacancyRate% Annual']:.2%}   (expect 6.00%)")
    print(f"  Maintenance:  {row['Maintenance% Annual']:.2%}   (expect 9.00%)")
    print(f"  Management:   {row['Management Fee']:.2%}   (expect 8.00%)")
    print(f"  Tax rate:     {row['PropertyTaxRate Annual']:.2%}   (expect 2.10%)")
    print(f"  Insurance:    ${row['Insurance Yearly']:,.2f}   (expect $1,900.00)")
    print(f"  HOA:          ${row['HOA Monthly']:,.2f}   (expect $200.00)")

    