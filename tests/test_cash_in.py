"""Rental 'cash you put in' = down payment + closing costs + repairs + points
(hand-checked: IL condo $240,000, 25% down, closing 3.75%, 3 points on $180,000)."""
import pytest
from engine.analyze import analyze_deal

DEAL = dict(model="Rental", state="Illinois", property_type="Condo", scenario="Base",
            price=240000, down_pct=0.25, annual_rate=0.078, rehab=0, base_rent=2400,
            exit_year=7, target_irr=0.15)


def test_cash_in_no_points():
    r = analyze_deal(**DEAL)
    assert r["down_payment"] == pytest.approx(60000)
    assert r["closing_costs"] == pytest.approx(9000)
    assert r["cash_in"] == pytest.approx(69000)


def test_cash_in_with_points_and_repairs():
    r = analyze_deal(**{**DEAL, "rehab": 10000}, points=3)
    assert r["points_cost"] == pytest.approx(5400)
    assert r["cash_in"] == pytest.approx(60000 + 9000 + 10000 + 5400)


def test_cash_in_matches_cash_return():
    r = analyze_deal(**DEAL, points=3)
    y1 = r["cash_flow_table"][0]["cash_flow"]
    assert r["cash_on_cash"] == pytest.approx(y1 / r["cash_in"], rel=1e-6)
