"""
DSCR the way DSCR lenders size it: gross rent / PITIA (Nov 2026, from
lender feedback). Plus the user's DSCR minimum and the optional
property tax / insurance boxes.
"""
import pytest
from engine.analyze import analyze_deal
from engine.solvers import max_price_dscr
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import B01
from tests.test_regression_flip import CASES as FLIP

R02 = RENTAL["R-02"]


def _pi(loan, rate):
    i = rate / 12
    return loan * i / (1 - (1 + i) ** -360)


def test_r02_dscr_by_hand():
    # 2,300 / (1,653.93 P&I + 623.33 tax + 150.00 insurance + 0 HOA)
    r = analyze_deal(**R02)
    pitia = _pi(255000, 0.0675) + 340000 * 0.022 / 12 + 1800 / 12
    assert r["pitia"] == pytest.approx(2427.26, abs=0.01)
    assert r["pitia"] == pytest.approx(pitia, abs=1e-9)
    assert r["min_dscr"] == pytest.approx(2300 / pitia, abs=1e-9)


def test_pitia_pieces_add_up():
    r = analyze_deal(**R02)
    total = r["pi_monthly"] + r["tax_monthly"] + r["insurance_monthly"] + r["hoa_monthly"]
    assert r["pitia"] == pytest.approx(total)


def test_b01_dscr_by_hand():
    # new loan 255,000 at 7.25%; tax on the 250,000 price
    r = analyze_deal(**B01)
    pitia = _pi(255000, 0.0725) + 250000 * 0.022 / 12 + 1800 / 12
    assert r["dscr"] == pytest.approx(2400 / pitia, abs=1e-9)


def test_default_minimum_is_one():
    assert analyze_deal(**R02)["dscr_min"] == 1.00


@pytest.mark.parametrize("minimum, expected", [
    (1.00, "REJECT"),        # R-03 DSCR 1.11 passes; IRR fails badly
    (1.20, "HARD REJECT"),   # same deal, stricter lender
])
def test_minimum_moves_the_gate(minimum, expected):
    assert analyze_deal(**{**RENTAL["R-03"], "dscr_min": minimum})["verdict"] == expected


def test_brrr_minimum_moves_the_gate():
    assert analyze_deal(**B01)["verdict"] != "HARD REJECT"           # 1.02 >= 1.00
    assert analyze_deal(**B01, dscr_min=1.10)["verdict"] == "HARD REJECT"


def test_solver_uses_the_deals_minimum():
    low = max_price_dscr(R02)["price"]
    high = max_price_dscr({**R02, "dscr_min": 1.25})["price"]
    assert high < low
    at = analyze_deal(**{**R02, "dscr_min": 1.25, "price": high})
    assert at["min_dscr"] == pytest.approx(1.25, abs=1e-6)


def test_tax_override_is_exact_dollars():
    r = analyze_deal(**R02, tax_override=6000)
    assert r["tax_monthly"] == pytest.approx(500.00)


def test_insurance_override_is_exact_dollars():
    r = analyze_deal(**R02, insurance_override=2400)
    assert r["insurance_monthly"] == pytest.approx(200.00)


def test_override_equal_to_default_changes_nothing():
    base = analyze_deal(**R02)
    same = analyze_deal(**R02, tax_override=340000 * 0.022, insurance_override=1800)
    assert same["irr"] == pytest.approx(base["irr"], abs=1e-12)
    assert same["min_dscr"] == pytest.approx(base["min_dscr"], abs=1e-12)


def test_lower_tax_raises_dscr_and_irr():
    base = analyze_deal(**R02)
    low = analyze_deal(**R02, tax_override=4000)
    assert low["min_dscr"] > base["min_dscr"]
    assert low["irr"] > base["irr"]


def test_brrr_overrides():
    r = analyze_deal(**B01, tax_override=3000, insurance_override=1200)
    assert r["tax_monthly"] == pytest.approx(250.00)
    assert r["insurance_monthly"] == pytest.approx(100.00)


def test_flip_insurance_override_raises_cost():
    deal = next(iter(FLIP.values()))
    base = analyze_deal(**deal)
    more = analyze_deal(**deal, insurance_override=10000)
    assert more["total_project_cost"] > base["total_project_cost"]


@pytest.mark.parametrize("bad", [
    {"tax_override": -1},
    {"insurance_override": -1},
    {"dscr_min": 0},
])
def test_bad_values_rejected(bad):
    with pytest.raises(ValueError):
        analyze_deal(**R02, **bad)
