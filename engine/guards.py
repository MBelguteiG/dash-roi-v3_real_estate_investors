"""
Input guards for Dash ROI v3 (Week 17).

Reject impossible inputs with a clear message BEFORE any engine runs,
so bad input fails loudly instead of producing quietly wrong numbers.
Called once, at the top of analyze_deal() - the single entry point used by
the UI, the solvers, and crosscheck.

All rates and percentages are DECIMALS (0.071, not 7.1) - this also catches
the v2 B9/B21 unit trap (whole number vs decimal).
"""


def _positive(inputs, key):
    if inputs[key] <= 0:
        raise ValueError(f"{key} must be greater than 0 (got {inputs[key]})")


def _non_negative(inputs, key):
    if inputs[key] < 0:
        raise ValueError(f"{key} cannot be negative (got {inputs[key]})")


def _fraction(inputs, key, allow_zero=True):
    v = inputs[key]
    low_ok = v >= 0 if allow_zero else v > 0
    if not (low_ok and v < 1):
        raise ValueError(f"{key} must be a decimal between 0 and 1, "
                         f"e.g. 0.071 for 7.1% (got {v})")


def _whole_at_least(inputs, key, minimum):
    v = inputs[key]
    if v != int(v) or v < minimum:
        raise ValueError(f"{key} must be a whole number >= {minimum} (got {v})")


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
            raise ValueError(f"refi_month ({inputs['refi_month']}) must come before "
                             f"the exit (month {inputs['exit_year'] * 12})")

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