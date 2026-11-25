"""Nov 25, 2026 fixes: Rental cash flow subtracts the full loan payment, and the
sale value grows for every year held. IL condo, $240,000, 25% down, 7.8%,
$2,400 rent, 7 years, Base. Hand check (separate code): loan payment = P&I on
$180,000 at 7.8% x 12; sale = 240,000 x (1+appr)^7, less selling costs and the
month-84 balance = $105,550.84; IRR by scipy brentq -> 4.6834%.
Year 1: -2,173 / 69,000 = -3.15%."""
import pytest
from engine.analyze import analyze_deal

DEAL = dict(model="Rental", state="Illinois", property_type="Condo", scenario="Base",
            price=240000, down_pct=0.25, annual_rate=0.078, rehab=0, base_rent=2400,
            exit_year=7, target_irr=0.15)


def test_irr_by_hand():
    r = analyze_deal(**DEAL)
    assert r["cash_flow_table"][-1]["sale_proceeds"] == pytest.approx(105550.84, abs=0.01)
    assert r["irr"] == pytest.approx(0.046834, abs=5e-7)


def test_users_townhouse_deal():
    # IL townhouse, Conservative, $280,000, 20% down, 7.9% with 3 points, 4 years.
    # Hand: sale 280,000 x 1.02^4 = 303,081 x 0.92 - balance 214,129.10 = 64,705.43
    r = analyze_deal(model="Rental", state="Illinois", property_type="Townhouse",
                     scenario="Conservative", price=280000, down_pct=0.20,
                     annual_rate=0.079, rehab=0, base_rent=2500, exit_year=4,
                     target_irr=0.10, points=3)
    assert r["cash_flow_table"][-1]["sale_proceeds"] == pytest.approx(64705.43, abs=0.01)
    assert r["irr"] == pytest.approx(-0.134158, abs=5e-7)


def test_first_year_cash_return_by_hand():
    r = analyze_deal(**DEAL)
    y1 = r["cash_flow_table"][0]
    assert y1["cash_flow"] == pytest.approx(y1["noi"] - r["annual_debt_service"]
                                            - y1["capex_reserve"])
    assert r["cash_on_cash"] == pytest.approx(-0.031496, abs=5e-7)


def test_old_v2_method_still_available():
    r = analyze_deal(**DEAL, v2_method=True)
    assert r["irr"] == pytest.approx(0.0590, abs=5e-5)     # what the app showed before


def test_fix_lowers_return():
    assert analyze_deal(**DEAL)["irr"] < analyze_deal(**DEAL, v2_method=True)["irr"]
