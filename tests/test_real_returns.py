import pytest
from engine.analyze import analyze_deal
from engine.irr import deflate
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import B01

R02 = RENTAL["R-02"]


@pytest.mark.parametrize("deal", [R02, B01], ids=["Rental", "BRRR"])
def test_real_irr_matches_exact_formula(deal):
    # Deflating every flow gives exactly (1 + nominal) / (1 + inflation) - 1
    r = analyze_deal(**deal)
    expected = (1 + r["irr"]) / (1 + r["inflation"]) - 1
    assert r["real_irr"] == pytest.approx(expected, abs=1e-7)


@pytest.mark.parametrize("deal", [R02, B01], ids=["Rental", "BRRR"])
def test_real_below_nominal_when_inflation_positive(deal):
    r = analyze_deal(**deal)
    assert r["inflation"] > 0
    assert r["real_irr"] < r["irr"]


def test_deflate_zero_inflation_is_identity():
    stream = [-100.0, 10.0, 20.0, 130.0]
    assert deflate(stream, 0.0) == stream


def test_deflate_matches_v2_return_analysis():
    # v2 Return Analysis: -4,645.65 / 1.02 = -4,554.55; -4,421.31 / 1.02^2 = -4,249.63
    real = deflate([-140375.00, -4645.65, -4421.31], 0.02)
    assert real[1] == pytest.approx(-4554.55, abs=0.01)
    assert real[2] == pytest.approx(-4249.63, abs=0.01)