"""Estimated APR (Reg Z actuarial idea: points + lender fees, title/appraisal left out).
Expected values hand-checked with scipy brentq, separate from engine/apr.py."""
import pytest
from engine.apr import estimated_apr
from engine.analyze import analyze_deal

DEAL = dict(model="Rental", state="Illinois", property_type="Condo", scenario="Base",
            price=240000, down_pct=0.25, annual_rate=0.078, rehab=0, base_rent=2400,
            exit_year=7, target_irr=0.15)


def test_no_fees_apr_equals_rate():
    assert estimated_apr(180000, 0.078, 0) == pytest.approx(0.078, abs=1e-9)


def test_two_percent_fees():
    assert estimated_apr(180000, 0.078, 3600) == pytest.approx(0.0801143283, abs=1e-9)


def test_rental_points_and_fees():
    r = analyze_deal(**DEAL, points=3, lender_fees=1500)
    assert r["rate_used"] == pytest.approx(0.0705)
    assert r["apr"] == pytest.approx(0.0744303114, abs=1e-9)


def test_fees_do_not_change_returns():
    a = analyze_deal(**DEAL, points=3)
    b = analyze_deal(**DEAL, points=3, lender_fees=1500)
    assert a["irr"] == b["irr"] and a["cash_on_cash"] == b["cash_on_cash"]
    assert a["apr"] == pytest.approx(0.0735546391, abs=1e-9)


def test_brrr_apr_on_refi_loan():
    r = analyze_deal(model="BRRR", state="Illinois", property_type="SFH", scenario="Base",
                     price=200000, rehab=25000, arv=300000, base_rent=2100, exit_year=4,
                     target_irr=0.10, hm_ltv=0.80, hm_rate=0.12, refi_ltv=0.75,
                     refi_month=6, post_refi_rate=0.068, lender_fees=2250)
    assert r["refi_loan"] == pytest.approx(225000)
    assert r["apr"] == pytest.approx(estimated_apr(225000, 0.068, 2250))
    assert r["apr"] > 0.068


def test_bad_fees():
    with pytest.raises(ValueError):
        analyze_deal(**DEAL, lender_fees=-1)
    with pytest.raises(ValueError):
        estimated_apr(1000, 0.07, 1000)
