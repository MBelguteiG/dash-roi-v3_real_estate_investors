"""
Input guards for Dash ROI v3 (Week 17).

Reject impossible inputs with a clear message BEFORE any engine runs,
so bad input fails loudly instead of producing quietly wrong numbers.
Called once, at the top of analyze_deal() - the single entry point used by
the UI, the solvers, and crosscheck.

All rates and percentages are DECIMALS (0.071, not 7.1) - this also catches
the v2 B9/B21 unit trap (whole number vs decimal).
"""


LABELS = {
    "price": "Price",
    "rehab": "Repair budget",
    "base_rent": "Rent / mo",
    "down_pct": "Down payment %",
    "annual_rate": "Loan rate %",
    "exit_year": "Years you'll own it",
    "arv": "Value after repairs",
    "hm_ltv": "Short-term loan %",
    "hm_rate": "Short-term rate %",
    "refi_ltv": "New loan % of value",
    "post_refi_rate": "New loan rate %",
    "refi_month": "Months to refinance",
    "points_pct": "Lender fee %",
    "hold_months": "Months to fix and sell",
    "monthly_utilities": "Utilities / mo",
    "monthly_maint_security": "Upkeep & security / mo",
    "target_margin": "Profit goal %",
}


def _label(key):
    return LABELS.get(key, key)


def _positive(inputs, key):
    if inputs[key] <= 0:
        raise ValueError(f"{_label(key)} must be more than 0.")


def _non_negative(inputs, key):
    if inputs[key] < 0:
        raise ValueError(f"{_label(key)} can't be negative.")


def _fraction(inputs, key, allow_zero=True):
    v = inputs[key]
    low_ok = v >= 0 if allow_zero else v > 0
    if not (low_ok and v < 1):
        low = "0% or more" if allow_zero else "more than 0%"
        raise ValueError(f"{_label(key)} must be {low} and less than 100% "
                         f"(you entered {v * 100:g}%).")


def _whole_at_least(inputs, key, minimum):
    v = inputs[key]
    if v != int(v) or v < minimum:
        raise ValueError(f"{_label(key)} must be a whole number, {minimum} or more.")

def validate_inputs(model, inputs):
    """Raise ValueError on the first impossible input; return None if all good."""
    _positive(inputs, "price")
    _non_negative(inputs, "rehab")

    if model == "Rental":
        _positive(inputs, "base_rent")
        _fraction(inputs, "down_pct")                       # 1.0 = no loan -> DSCR breaks
        _fraction(inputs, "annual_rate", allow_zero=False)  # amortization needs a rate
        _whole_at_least(inputs, "exit_year", 1)

    elif model == "BRRR":
        _positive(inputs, "base_rent")
        _positive(inputs, "arv")
        _fraction(inputs, "hm_ltv", allow_zero=False)
        _fraction(inputs, "hm_rate")
        _fraction(inputs, "refi_ltv", allow_zero=False)
        _fraction(inputs, "post_refi_rate", allow_zero=False)
        _whole_at_least(inputs, "exit_year", 1)
        _whole_at_least(inputs, "refi_month", 1)
        if inputs["refi_month"] >= inputs["exit_year"] * 12:
            raise ValueError(f"Months to refinance ({inputs['refi_month']}) must be "
                             f"before you sell (month {inputs['exit_year'] * 12}).")

    elif model == "Flip":
        _positive(inputs, "arv")
        _fraction(inputs, "hm_ltv", allow_zero=False)
        _fraction(inputs, "hm_rate")
        _fraction(inputs, "points_pct")
        _whole_at_least(inputs, "hold_months", 1)          # 0 -> annualized ROI breaks
        _non_negative(inputs, "monthly_utilities")
        _non_negative(inputs, "monthly_maint_security")
        _fraction(inputs, "target_margin", allow_zero=False)


# --- Tests: every bad input must be caught; every reference deal must pass ---
if __name__ == "__main__":
    from engine.crosscheck import DEALS
    from engine.analyze import analyze_deal

    bad_cases = [
        ("Rental rate typed as 7.1",    {**DEALS["Rental"], "annual_rate": 7.1}),
        ("Rental 100% down",            {**DEALS["Rental"], "down_pct": 1.0}),
        ("Rental negative price",       {**DEALS["Rental"], "price": -5}),
        ("BRRR refi after exit",        {**DEALS["BRRR"], "refi_month": 70}),
        ("BRRR exit 2.5 years",         {**DEALS["BRRR"], "exit_year": 2.5}),
        ("Flip 0-month hold",           {**DEALS["Flip"], "hold_months": 0}),
        ("Flip margin typed as 13",     {**DEALS["Flip"], "target_margin": 13}),
    ]
    print("=== Bad inputs (each must be caught) ===\n")
    for label, bad in bad_cases:
        try:
            analyze_deal(**bad)
            print(f"NOT CAUGHT  {label}")
        except ValueError as e:
            print(f"caught      {label:<26} -> {e}")

    print("\n=== Reference deals (each must pass) ===\n")
    for name, deal in DEALS.items():
        analyze_deal(**deal)
        print(f"OK          {name}")