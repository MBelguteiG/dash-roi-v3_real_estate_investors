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
    "B-03": dict(model="BRRR", state="California", property_type="SFH",
                 scenario="Base", price=450000, rehab=60000, base_rent=3200,
                 exit_year=5, target_irr=0.10, arv=620000, hm_ltv=0.90,
                 hm_rate=0.105, refi_ltv=0.70, refi_month=6,
                 post_refi_rate=0.0725),

        # B-04: rent 2300 inferred from v2's recorded IRR of 36.69%
    "B-04-650": dict(model="BRRR", state="California", property_type="SFH",
                scenario="Base", price=400000, rehab=60000, base_rent=2300,
                exit_year=5, target_irr=0.10, arv=650000, hm_ltv=0.90,
                hm_rate=0.105, refi_ltv=0.80, refi_month=6,
                post_refi_rate=0.0725),

}

CASES["B-04-750"] = {**CASES["B-04-650"], "arv": 750000}



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
    

    # B-03: v2 showed IRR 12.76%, DSCR 0.60, HARD REJECT (strong IRR, fails DSCR gate)
    ("B-03", "irr", 0.12805, 0.00005),
    ("B-03", "cash_invested", 117375.00, 0.01),
    ("B-03", "cash_pulled_out", 29000.00, 0.01),
    ("B-03", "cash_left", 88375.00, 0.01),
    ("B-03", "dscr", 0.5954, 0.0005),
    ("B-03", "required_rent", 6036.77, 0.01),
    ("B-03", "rent_cushion", -2836.77, 0.01),
    ("B-03", "sale_price", 739676.32, 0.01),
    ("B-03", "equity_at_exit", 327217.37, 0.01),
    ("B-03", "verdict", "HARD REJECT", None),
    
    # B-04 at ARV 650K: v2 showed IRR 36.69% and no guard (its display then
    # checked IRR > 100% only); v3 flags it because cash left is negative
    ("B-04-650", "irr", 0.36748, 0.00005),
    ("B-04-650", "cash_invested", 111000.00, 0.01),
    ("B-04-650", "cash_pulled_out", 160000.00, 0.01),
    ("B-04-650", "cash_left", -49000.00, 0.01),
    ("B-04-650", "all_cash_out", True, None),
    ("B-04-650", "dscr", 0.3131, 0.0005),
    ("B-04-650", "verdict", "HARD REJECT", None),
    # B-04 at ARV 750K: v2 guard fired on IRR > 100%
    ("B-04-750", "irr", 2.02709, 0.00005),
    ("B-04-750", "cash_pulled_out", 240000.00, 0.01),
    ("B-04-750", "cash_left", -129000.00, 0.01),
    ("B-04-750", "all_cash_out", True, None),
    ("B-04-750", "verdict", "HARD REJECT", None),
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