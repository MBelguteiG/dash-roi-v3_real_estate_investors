import pytest
from engine.analyze import analyze_deal

CASES = {
    "R-02": dict(model="Rental", state="Illinois", property_type="SFH",
                 scenario="Base", price=340000, down_pct=0.25,
                 annual_rate=0.0675, rehab=0, base_rent=2300,
                 exit_year=5, target_irr=0.08),
    "R-01": dict(model="Rental", state="California", property_type="SFH",
                 scenario="Base", price=500000, down_pct=0.25,
                 annual_rate=0.0675, rehab=0, base_rent=2400,
                 exit_year=5, target_irr=0.08),
    "R-03": dict(model="Rental", state="Illinois", property_type="SFH",
                 scenario="Base", price=300000, down_pct=0.25,
                 annual_rate=0.0675, rehab=0, base_rent=2400,
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
     # R-01: v3-only values, not yet verified against the v2 workbook
    ("R-01", "irr", -0.00301, 0.00005),
    ("R-01", "cash_on_cash", -0.09466, 0.00005),
    ("R-01", "min_dscr", 0.46, 0.005),
    ("R-01", "required_rent", 4969.16, 0.01),
    ("R-01", "rent_cushion", -2569.16, 0.01),
    ("R-01", "verdict", "HARD REJECT", None), 
    # R-03: DSCR, required rent, verdict match v2; irr and cash_on_cash are v3-only
    ("R-03", "irr", 0.00094, 0.00005),
    ("R-03", "cash_on_cash", -0.04223, 0.00005),
    ("R-03", "min_dscr", 0.77, 0.005),
    ("R-03", "required_rent", 3552.49, 0.01),
    ("R-03", "rent_cushion", -1152.49, 0.01),
    ("R-03", "verdict", "HARD REJECT", None),
    


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