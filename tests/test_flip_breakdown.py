"""Flip fix + cost breakdown (Nov 25, 2026). BDash's IL townhouse flip, Base:
$200,000, repairs $40,000, sale $320,000, 6 months, 75% short-term loan at 12%,
1% lender fee, utilities $250, upkeep $200. Hand-checked:
down 50,000 + closing 3.75% 7,500 + fee 1,500 + repairs 40,000 + interest
150,000 x 1% x 6 = 9,000 + holding (350 + 116.67 + 200 + 250 + 200) x 6 = 6,700
-> cash in 114,700 (selling costs left out). Sale: 320,000 - 7% 22,400 - 150,000
= 147,600 back; profit 147,600 - 114,700 = 32,900; 32,900 / 114,700 = 28.68%."""
import pytest
from engine.analyze import analyze_deal

DEAL = dict(model="Flip", state="Illinois", property_type="Townhouse", scenario="Base",
            price=200000, rehab=40000, arv=320000, hm_ltv=0.75, hm_rate=0.12,
            hold_months=6, points_pct=0.01, monthly_utilities=250,
            monthly_maint_security=200, target_margin=0.10)
R = analyze_deal(**DEAL)


@pytest.mark.parametrize("key, expected", [
    ("down_payment", 50000), ("closing_costs", 7500), ("hm_points", 1500),
    ("hm_interest", 9000), ("total_holding", 6700), ("cash_invested", 114700),
    ("selling_cost", 22400), ("cash_back_at_sale", 147600), ("net_profit", 32900)])
def test_by_hand(key, expected):
    assert R[key] == pytest.approx(expected, abs=0.01)


def test_profit_is_cash_back_minus_cash_in():
    assert R["cash_back_at_sale"] - R["cash_invested"] == pytest.approx(R["net_profit"])


def test_returns_by_hand():
    assert R["roi_on_cash"] == pytest.approx(32900 / 114700)
    assert R["annualized_roi"] == pytest.approx(32900 / 114700 * 2)


def test_holding_pieces_add_up():
    m = (R["tax_monthly"] + R["insurance_monthly"] + R["hoa_monthly"]
         + R["utilities_monthly"] + R["upkeep_monthly"])
    assert m * 6 == pytest.approx(R["total_holding"])


def test_v2_method_kept():
    r = analyze_deal(**DEAL, v2_method=True)
    assert r["cash_invested"] == pytest.approx(137100)        # old: selling costs counted
    assert r["annualized_roi"] == pytest.approx(0.4799, abs=5e-5)
    assert r["net_profit"] == R["net_profit"] and r["verdict"] == R["verdict"]
