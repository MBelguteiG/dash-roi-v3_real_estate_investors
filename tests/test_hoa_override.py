import pytest
from engine.analyze import analyze_deal
from engine.assumptions import get_assumptions
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import CASES as BRRR
from tests.test_regression_flip import CASES as FLIP

R02, B01, F01B = RENTAL["R-02"], BRRR["B-01"], FLIP["F-01b"]


def default_hoa(deal):
    a = get_assumptions(deal["state"], deal["property_type"],
                        deal["model"], deal["scenario"])
    return a["HOA Monthly"]


@pytest.mark.parametrize("deal", [R02, B01, F01B], ids=["Rental", "BRRR", "Flip"])
def test_override_equal_to_default_changes_nothing(deal):
    base = analyze_deal(**deal)
    same = analyze_deal(**deal, hoa_override=default_hoa(deal))
    assert same == base


def test_flip_condo_holding_drops_by_the_hoa():
    # F-01b CA Condo: v2 holding 1,195.83 includes the $400 default HOA
    r = analyze_deal(**F01B, hoa_override=0)
    assert r["monthly_holding"] == pytest.approx(1195.83 - default_hoa(F01B), abs=0.01)


def test_rental_higher_hoa_lowers_noi_and_dscr():
    base = analyze_deal(**R02)
    up = analyze_deal(**R02, hoa_override=default_hoa(R02) + 200)
    assert up["noi_y1"] < base["noi_y1"]
    assert up["min_dscr"] < base["min_dscr"]


def test_brrr_higher_hoa_lowers_dscr():
    base = analyze_deal(**B01)
    up = analyze_deal(**B01, hoa_override=default_hoa(B01) + 200)
    assert up["dscr"] < base["dscr"]


def test_negative_hoa_rejected():
    with pytest.raises(ValueError):
        analyze_deal(**R02, hoa_override=-50)