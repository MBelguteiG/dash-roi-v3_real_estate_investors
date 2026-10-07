import pytest
from engine.analyze import analyze_deal

F01 = dict(model="Flip", state="California", property_type="SFH",
           scenario="Base", price=450000, rehab=70000, arv=650000,
           hm_ltv=0.90, hm_rate=0.105, hold_months=6, points_pct=0.02,
           monthly_utilities=150.0, monthly_maint_security=150.0,
           target_margin=0.15)

CASES = {
    "F-01a": F01,
    "F-01b": {**F01, "property_type": "Condo"},
    "F-01c": {**F01, "property_type": "Townhouse"},
    "F-01d": {**F01, "property_type": "Duplex"},
}

# (case, output key, expected, tolerance)
CHECKS = [
    # F-01a SFH: v2 showed ROI 39.04%, margin 6.16%, net profit 40,013, REJECT
    ("F-01a", "monthly_holding", 1000.00, 0.01),
    ("F-01a", "net_profit", 40012.50, 0.01),
    ("F-01a", "annualized_roi", 0.39039, 0.00005),
    ("F-01a", "profit_margin", 0.06156, 0.00005),
    ("F-01a", "verdict", "REJECT", None),
    # F-01b Condo: v2 showed holding 1,195.83, ROI 37.68%, margin 5.98%, REJECT
    ("F-01b", "monthly_holding", 1195.83, 0.01),
    ("F-01b", "net_profit", 38837.50, 0.01),
    ("F-01b", "annualized_roi", 0.37677, 0.00005),
    ("F-01b", "profit_margin", 0.05975, 0.00005),
    ("F-01b", "verdict", "REJECT", None),
    # F-01c Townhouse: v2 showed holding 1,156.25, ROI 37.95%, margin 6.01%, REJECT
    ("F-01c", "monthly_holding", 1156.25, 0.01),
    ("F-01c", "net_profit", 39075.00, 0.01),
    ("F-01c", "annualized_roi", 0.37951, 0.00005),
    ("F-01c", "profit_margin", 0.06012, 0.00005),
    ("F-01c", "verdict", "REJECT", None),
    # F-01d Duplex: v2 showed holding 968.75, ROI 39.26%, margin 6.18%, REJECT
    ("F-01d", "monthly_holding", 968.75, 0.01),
    ("F-01d", "net_profit", 40200.00, 0.01),
    ("F-01d", "annualized_roi", 0.39258, 0.00005),
    ("F-01d", "profit_margin", 0.06185, 0.00005),
    ("F-01d", "verdict", "REJECT", None),
]

RESULTS = {name: analyze_deal(**inputs) for name, inputs in CASES.items()}
IDS = [f"{c[0]}-{c[1]}" for c in CHECKS]


@pytest.mark.parametrize("case, key, expected, tol", CHECKS, ids=IDS)
def test_flip_regression(case, key, expected, tol):
    actual = RESULTS[case][key]
    if tol is None:
        assert actual == expected
    else:
        assert actual == pytest.approx(expected, abs=tol)