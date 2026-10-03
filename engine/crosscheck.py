"""
M3 cross-check for Dash ROI v3: every engine vs the v2 Excel workbook.

Runs the three reference deals through analyze_deal() (the same entry point
the UI calls) and labels each output:
  MATCH       - equals the v2 value (within display rounding)
  DOCUMENTED  - intentionally differs from v2; equals the recorded v3 value
  FAIL        - anything else
A DOCUMENTED line still FAILS if v3 drifts from its recorded value, so
intentional upgrades are protected from accidental regressions too.

Note: v2 values are only valid with Main_Dashboard B4 set to that model
(v2 Property_inputs uses B4's assumptions for every block).
"""

import sys
from engine.analyze import analyze_deal

DEALS = {
    "Rental": dict(model="Rental", state="Illinois", property_type="Townhouse",
                   scenario="Conservative", price=250000, down_pct=0.30,
                   annual_rate=0.078, rehab=28000, base_rent=2750,
                   exit_year=5, target_irr=0.15),
    "BRRR": dict(model="BRRR", state="California", property_type="Townhouse",
                 scenario="Base", price=650000, rehab=25000, base_rent=4500,
                 exit_year=5, target_irr=0.13, arv=800000, hm_ltv=0.85,
                 hm_rate=0.12, refi_ltv=0.75, refi_month=6, post_refi_rate=0.09),
    "Flip": dict(model="Flip", state="California", property_type="Townhouse",
                 scenario="Base", price=650000, rehab=25000, arv=800000,
                 hm_ltv=0.85, hm_rate=0.12, hold_months=5, points_pct=0.02,
                 monthly_utilities=150.00, monthly_maint_security=150.00,
                 target_margin=0.13),
}

PCT = 0.00005   # % shown to 2 decimals in v2
USD = 0.01      # dollars shown to cents
UPG = "HOA/maint escalation + rent-linked CapEx"

# (model, output key, v2 value, v3 documented value or None, tolerance, reason)
CHECKS = [
    ("Rental", "irr",                 -0.0514,    -0.0539,   PCT, UPG),
    ("Rental", "cash_on_cash",        -0.0004,    None,      PCT, ""),
    ("Rental", "min_dscr",            1.05,       None,      0.005, ""),
    ("Rental", "required_rent",       3296.52,    None,      USD, ""),
    ("Rental", "rent_cushion",        -546.52,    None,      USD, ""),
    ("Rental", "verdict",             "REJECT",   None,      None, ""),

    ("BRRR", "irr",                   0.0742,     0.0740,    PCT, UPG + " + B34 fix"),
    ("BRRR", "cash_invested",         140375.00,  None,      USD, ""),
    ("BRRR", "cash_pulled_out",       47500.00,   None,      USD, ""),
    ("BRRR", "cash_left",             92875.00,   None,      USD, ""),
    ("BRRR", "post_refi_cash_flow",   -29850.95,  -29937.35, USD, UPG),
    ("BRRR", "cash_on_cash",          -0.3214,    -0.3223,   PCT, UPG),
    ("BRRR", "dscr",                  0.528,      None,      0.0005, ""),
    ("BRRR", "dscr_with_reserves",    0.472,      None,      0.0005, ""),
    ("BRRR", "required_rent",         7420.79,    9216.38,   USD, "v2 bug: uses purchase loan, not refi"),
    ("BRRR", "rent_cushion",          -2920.79,   -4716.38,  USD, "v2 bug: uses purchase loan, not refi"),
    ("BRRR", "sale_price",            954421.06,  None,      USD, ""),
    ("BRRR", "equity_at_exit",        375653.71,  376140.69, USD, "v2 B34 double-counts final principal"),
    ("BRRR", "verdict",               "HARD REJECT", None,   None, ""),

    ("Flip", "hm_loan",               552500.00,  None,      USD, ""),
    ("Flip", "hm_interest",           27625.00,   None,      USD, ""),
    ("Flip", "hm_points",             11050.00,   None,      USD, ""),
    ("Flip", "closing_costs",         17875.00,   None,      USD, ""),
    ("Flip", "monthly_holding",       1347.92,    None,      USD, ""),
    ("Flip", "total_holding",         6739.58,    None,      USD, ""),
    ("Flip", "selling_cost",          52000.00,   None,      USD, ""),
    ("Flip", "total_project_cost",    790289.58,  None,      USD, ""),
    ("Flip", "net_profit",            9710.42,    None,      USD, ""),
    ("Flip", "cash_invested",         237789.58,  None,      USD, ""),
    ("Flip", "roi_on_cash",           0.0408,     None,      PCT, ""),
    ("Flip", "annualized_roi",        0.0980,     None,      PCT, ""),
    ("Flip", "profit_margin",         0.0121,     None,      PCT, ""),
    ("Flip", "max_offer_mao",         555710.42,  None,      USD, ""),
    ("Flip", "max_offer_70pct",       535000.00,  None,      USD, ""),
    ("Flip", "over_under_mao",        94289.58,   None,      USD, ""),
    ("Flip", "verdict",               "REJECT",   None,      None, ""),
]


def close(actual, expected, tol):
    """Exact for text (verdicts); within tolerance for numbers."""
    if tol is None:
        return actual == expected
    return abs(actual - expected) <= tol


def fmt(x):
    if isinstance(x, str):
        return x
    return f"{x:.4f}" if abs(x) < 10 else f"{x:,.2f}"


def run():
    results = {m: analyze_deal(**inputs) for m, inputs in DEALS.items()}
    counts = {"MATCH": 0, "DOCUMENTED": 0, "FAIL": 0}

    print("=== Dash ROI v3 - M3 cross-check vs v2 Excel ===\n")
    for model, key, v2, v3_doc, tol, reason in CHECKS:
        actual = results[model][key]
        if v3_doc is None:
            status = "MATCH" if close(actual, v2, tol) else "FAIL"
        else:
            status = "DOCUMENTED" if close(actual, v3_doc, tol) else "FAIL"
        counts[status] += 1
        note = f"  ({reason})" if status == "DOCUMENTED" else ""
        print(f"{status:<11}{model:<7}{key:<21}v3 {fmt(actual):>14}   v2 {fmt(v2):>14}{note}")

    print(f"\nM3: {counts['MATCH']} MATCH, {counts['DOCUMENTED']} DOCUMENTED, "
          f"{counts['FAIL']} FAIL  ({len(CHECKS)} checks)")
    return counts["FAIL"] == 0


if __name__ == "__main__":
    sys.exit(0 if run() else 1)