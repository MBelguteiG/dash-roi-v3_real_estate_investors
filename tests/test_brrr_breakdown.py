"""BRRR cost breakdown (Nov 24, 2026). IL townhouse, Conservative, hand-checked:
down 240,000-192,000 = 48,000; closing 3.75% = 9,000; repairs 25,000 -> 82,000.
Months 1-6: interest 192,000 x 1% x 6 = 11,520; tax 5,040/12 + insurance
1,900/12 + HOA 200 = 778.33/mo x 6 = 4,670. Refi: 243,750 - 192,000 - 6% (14,625)
= 37,125 back; 82,000 - 37,125 = 44,875 still in."""
import pytest
from engine.analyze import analyze_deal

DEAL = dict(model="BRRR", state="Illinois", property_type="Townhouse",
            scenario="Conservative", price=240000, rehab=25000, arv=325000,
            base_rent=2800, exit_year=5, target_irr=0.10, hm_ltv=0.80, hm_rate=0.12,
            refi_month=6, refi_ltv=0.75, post_refi_rate=0.078, refi_type="Cash-Out")
R = analyze_deal(**DEAL)


@pytest.mark.parametrize("key, expected", [
    ("down_payment", 48000), ("closing_costs", 9000), ("rehab", 25000),
    ("cash_invested", 82000), ("rehab_interest", 11520), ("rehab_carry", 4670),
    ("refi_loan", 243750), ("hm_loan", 192000), ("refi_cost", 14625),
    ("cash_pulled_out", 37125), ("cash_left", 44875)])
def test_breakdown_by_hand(key, expected):
    assert R[key] == pytest.approx(expected, abs=0.01)


def test_pieces_add_up():
    assert R["down_payment"] + R["closing_costs"] + R["rehab"] == pytest.approx(R["cash_invested"])
    back = R["refi_loan"] - R["hm_loan"] - R["refi_cost"] - R["points_cost"]
    assert back == pytest.approx(R["cash_pulled_out"])


def test_repair_months_match_cash_flow_table():
    # Year 1 rent-left and loan payments include months 1-6
    y1 = R["cash_flow_table"][0]
    assert y1["noi"] == pytest.approx(-R["rehab_carry"] + 6 * (1321.6667), abs=0.05)
    assert y1["debt_service"] == pytest.approx(R["rehab_interest"] + 6 * 1754.6765, abs=0.05)


# Equity after the refi (Nov 24): BDash's question - ARV 350,000, new loan 70%.
# By hand: equity 350,000 - 245,000 = 105,000 = money still in 53,400 + value
# created 350,000 - (250,000 + 28,000 + 9,375 + 11,025) = 51,600.
def test_equity_split_by_hand():
    d = {**DEAL, "scenario": "Base", "price": 250000, "rehab": 28000, "arv": 350000,
         "refi_month": 10, "refi_ltv": 0.70}
    r = analyze_deal(**d)
    assert r["equity_after_refi"] == pytest.approx(105000)
    assert r["cash_left"] == pytest.approx(53400)
    assert r["value_created"] == pytest.approx(51600)
    assert r["cash_left"] + r["value_created"] == pytest.approx(r["equity_after_refi"])


def test_equity_split_when_all_cash_comes_out():
    r = analyze_deal(**{**DEAL, "price": 180000})
    assert r["cash_left"] < 0
    assert r["cash_left"] + r["value_created"] == pytest.approx(r["equity_after_refi"])
