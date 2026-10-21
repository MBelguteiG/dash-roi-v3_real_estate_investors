import pytest
from engine.analyze import analyze_deal
from engine.amortization import annual_debt_service
from tests.test_regression_rental import CASES

R02 = CASES["R-02"]
BASE = analyze_deal(**R02)
ONE = analyze_deal(**R02, points=1.0)


def test_zero_points_changes_nothing():
    r = analyze_deal(**R02, points=0.0)
    for key in ("irr", "min_dscr", "cash_on_cash", "required_rent", "real_irr"):
        assert r[key] == pytest.approx(BASE[key], abs=1e-12)


def test_one_point_cost_and_rate():
    assert ONE["points_cost"] == pytest.approx(2550.00)          # 1% of $255,000
    assert ONE["rate_used"] == pytest.approx(0.0675 - 0.0025)


def test_saving_and_breakeven():
    saving = (annual_debt_service(255000, 0.0675)
              - annual_debt_service(255000, 0.0650)) / 12
    assert ONE["monthly_saving"] == pytest.approx(saving)
    assert ONE["breakeven_months"] == pytest.approx(2550 / saving)


def test_points_lower_payment_and_raise_dscr():
    assert ONE["annual_debt_service"] < BASE["annual_debt_service"]
    assert ONE["min_dscr"] > BASE["min_dscr"]


def test_negative_points_rejected():
    with pytest.raises(ValueError):
        analyze_deal(**R02, points=-1)