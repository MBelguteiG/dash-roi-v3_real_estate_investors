import pytest
from engine.analyze import analyze_deal
from engine.assumptions import get_assumptions
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import B01

R02 = RENTAL["R-02"]


def capex_rate(deal):
    a = get_assumptions(deal["state"], deal["property_type"], deal["model"], deal["scenario"])
    return a["CapEx% Annual"]


def test_rental_reserves_formula():
    r = analyze_deal(**R02)
    capex_y1 = R02["base_rent"] * 12 * capex_rate(R02)
    expected = (r["noi_y1"] - capex_y1) / r["annual_debt_service"]
    assert r["dscr_with_reserves"] == pytest.approx(expected, rel=1e-12)


def test_rental_reserves_below_plain_dscr():
    assert capex_rate(R02) > 0
    r = analyze_deal(**R02)
    plain_y1 = r["noi_y1"] / r["annual_debt_service"]
    assert r["dscr_with_reserves"] < plain_y1


def test_brrr_reserves_below_plain_dscr():
    r = analyze_deal(**B01)
    assert r["dscr_with_reserves"] < r["dscr"]


def test_rental_verdict_unchanged():
    # Reserves line is informational; it must not move the verdict
    assert analyze_deal(**R02)["verdict"] == "HARD REJECT"