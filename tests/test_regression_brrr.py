import pytest
from engine.analyze import analyze_deal

B01 = dict(model="BRRR", state="Illinois", property_type="SFH",
           scenario="Base", price=250000, rehab=45000, base_rent=2400,
           exit_year=5, target_irr=0.10, arv=340000, hm_ltv=0.90,
           hm_rate=0.105, refi_ltv=0.75, refi_month=6,
           post_refi_rate=0.0725)

CASES = {
    "B-01": B01,
    # B-08 was run in v2 with refi LTV at 65% (inferred from its recorded figures)
    "B-08": {**B01, "refi_ltv": 0.65},
}

# (case, output key, expected, tolerance)
CHECKS = [
    # B-01 / B-02: DSCR 0.70 and HARD REJECT match v2; other figures are v3-only
    ("B-01", "irr", 0.06104, 0.00005),
    ("B-01", "cash_invested", 79375.00, 0.01),
    ("B-01", "cash_pulled_out", 30000.00, 0.01),
    ("B-01", "cash_left", 49375.00, 0.01),
    ("B-01", "dscr", 0.70, 0.005),
    ("B-01", "required_rent", 3964.40, 0.01),
    ("B-01", "rent_cushion", -1564.40, 0.01),
    ("B-01", "sale_price", 388370.67, 0.01),
    ("B-01", "equity_at_exit", 146027.28, 0.01),
    ("B-01", "verdict", "HARD REJECT", None),
    # B-08: v2 showed equity 178,102.50 and proceeds 147,032.84;
    # v3 is 237.24 higher on both (documented B34 double-count fix)
    ("B-08", "equity_at_exit", 178339.74, 0.01),
    ("B-08", "net_sale_proceeds", 147270.08, 0.01),
    ("B-08", "remaining_balance", 210030.94, 0.01),
]

RESULTS = {name: analyze_deal(**inputs) for name, inputs in CASES.items()}
IDS = [f"{c[0]}-{c[1]}" for c in CHECKS]


@pytest.mark.parametrize("case, key, expected, tol", CHECKS, ids=IDS)
def test_brrr_regression(case, key, expected, tol):
    actual = RESULTS[case][key]
    if tol is None:
        assert actual == expected
    else:
        assert actual == pytest.approx(expected, abs=tol)