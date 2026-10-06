import pytest
from engine.analyze import analyze_deal

CASES = {
    "R-02": dict(model="Rental", state="Illinois", property_type="SFH",
                 scenario="Base", price=340000, down_pct=0.25,
                 annual_rate=0.0675, rehab=0, base_rent=2300,
                 exit_year=5, target_irr=0.08),
}

# (case, output key, expected, tolerance)
CHECKS = [
    ("R-02", "irr", -0.03185, 0.00005),  # v2 showed -3.19%; v3 documented
    ("R-02", "cash_on_cash", -0.07535, 0.00005),
    ("R-02", "min_dscr", 0.59, 0.005),
    ("R-02", "required_rent", 3997.16, 0.01),
    ("R-02", "rent_cushion", -1697.16, 0.01),
    ("R-02", "verdict", "HARD REJECT", None),
]

RESULTS = {name: analyze_deal(**inputs) for name, inputs in CASES.items()}
IDS = [f"{c[0]}-{c[1]}" for c in CHECKS]


@pytest.mark.parametrize("case, key, expected, tol", CHECKS, ids=IDS)
def test_rental_regression(case, key, expected, tol):
    actual = RESULTS[case][key]
    if tol is None:
        assert actual == expected
    else:
        assert actual == pytest.approx(expected, abs=tol)