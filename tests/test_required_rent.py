import pytest
from engine.analyze import analyze_deal
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import B01

R02 = RENTAL["R-02"]


def test_rental_lender_rent_gives_dscr_120():
    rent = analyze_deal(**R02)["required_rent_lender"]
    r = analyze_deal(**{**R02, "base_rent": rent})
    assert r["min_dscr"] == pytest.approx(1.20, abs=1e-4)


def test_rental_reserves_rent_gives_reserves_dscr_120():
    rent = analyze_deal(**R02)["required_rent"]
    r = analyze_deal(**{**R02, "base_rent": rent})
    assert r["dscr_with_reserves"] == pytest.approx(1.20, abs=1e-4)


def test_brrr_lender_rent_gives_dscr_120():
    rent = analyze_deal(**B01)["required_rent_lender"]
    r = analyze_deal(**{**B01, "base_rent": rent})
    assert r["dscr"] == pytest.approx(1.20, abs=1e-4)


@pytest.mark.parametrize("deal", [R02, B01], ids=["Rental", "BRRR"])
def test_lender_rent_below_reserves_rent(deal):
    r = analyze_deal(**deal)
    assert r["required_rent_lender"] < r["required_rent"]