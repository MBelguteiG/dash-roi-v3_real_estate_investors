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

F02 = dict(model="Flip", state="Illinois", property_type="SFH",
           scenario="Base", price=200000, rehab=55000, arv=340000,
           hm_ltv=0.90, hm_rate=0.105, hold_months=6, points_pct=0.02,
           monthly_utilities=150.0, monthly_maint_security=150.0,
           target_margin=0.15)
CASES["F-02a"] = F02
CASES["F-02b"] = {**F02, "property_type": "Condo"}
CASES["F-02c"] = {**F02, "property_type": "Townhouse"}
CASES["F-02d"] = {**F02, "property_type": "Duplex"}
CASES["F-02e"] = {**F02, "property_type": "Duplex", "price": 170000,
                  "target_margin": 0.18}



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

CHECKS += [
    # F-02a IL SFH: v2 showed ROI 57.86%, margin 10.56%, NEGOTIATE, MAO 184,900
    ("F-02a", "monthly_holding", 791.67, 0.01),
    ("F-02a", "net_profit", 35900.00, 0.01),
    ("F-02a", "annualized_roi", 0.57857, 0.00005),
    ("F-02a", "profit_margin", 0.10559, 0.00005),
    ("F-02a", "max_offer_mao", 184900.00, 0.01),
    ("F-02a", "over_under_mao", 15100.00, 0.01),
    ("F-02a", "verdict", "NEGOTIATE", None),
    # F-02b IL Condo: v2 showed ROI 55.90%, margin 10.28%, NEGOTIATE
    ("F-02b", "monthly_holding", 950.00, 0.01),
    ("F-02b", "net_profit", 34950.00, 0.01),
    ("F-02b", "annualized_roi", 0.55898, 0.00005),
    ("F-02b", "profit_margin", 0.10279, 0.00005),
    ("F-02b", "max_offer_mao", 183950.00, 0.01),
    ("F-02b", "over_under_mao", 16050.00, 0.01),
    ("F-02b", "verdict", "NEGOTIATE", None),
    # F-02c IL Townhouse: v2 showed ROI 55.69%, margin 10.25%, NEGOTIATE
    ("F-02c", "monthly_holding", 966.67, 0.01),
    ("F-02c", "net_profit", 34850.00, 0.01),
    ("F-02c", "annualized_roi", 0.55693, 0.00005),
    ("F-02c", "profit_margin", 0.10250, 0.00005),
    ("F-02c", "max_offer_mao", 183850.00, 0.01),
    ("F-02c", "over_under_mao", 16150.00, 0.01),
    ("F-02c", "verdict", "NEGOTIATE", None),
    # F-02d IL Duplex: v2 showed ROI 56.62%, margin 10.38%, NEGOTIATE
    ("F-02d", "monthly_holding", 891.67, 0.01),
    ("F-02d", "net_profit", 35300.00, 0.01),
    ("F-02d", "annualized_roi", 0.56616, 0.00005),
    ("F-02d", "profit_margin", 0.10382, 0.00005),
    ("F-02d", "max_offer_mao", 184300.00, 0.01),
    ("F-02d", "over_under_mao", 15700.00, 0.01),
    ("F-02d", "verdict", "NEGOTIATE", None),
    # F-02e IL Duplex at 170K, target 18%: v2 showed ROI 116.22%, margin 20.21%,
    # BUY, net profit 68,728, 7,527 under MAO
    ("F-02e", "monthly_holding", 834.17, 0.01),
    ("F-02e", "net_profit", 68727.50, 0.01),
    ("F-02e", "annualized_roi", 1.16219, 0.00005),
    ("F-02e", "profit_margin", 0.20214, 0.00005),
    ("F-02e", "max_offer_mao", 177527.50, 0.01),
    ("F-02e", "over_under_mao", -7527.50, 0.01),
    ("F-02e", "verdict", "BUY", None),
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

# F-03a-d: Flip has no DSCR block, whatever the property type
@pytest.mark.parametrize("case", ["F-01a", "F-01b", "F-01c", "F-01d"])
def test_flip_has_no_dscr_block(case):
    result = RESULTS[case]
    assert not any("dscr" in key for key in result)
    assert "required_rent" not in result
    assert "rent_cushion" not in result