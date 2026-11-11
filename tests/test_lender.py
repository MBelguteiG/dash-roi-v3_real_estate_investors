import pytest
from engine.analyze import analyze_deal
from engine.verdict import approval_likelihood
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_flip import CASES as FLIP


# Each tier at the default minimum (1.00), including the exact boundaries
@pytest.mark.parametrize("dscr, ltv, expected", [
    (1.25, 0.80, "STRONG"),
    (1.30, 0.81, "CONDITIONAL"),   # strong DSCR but LTV over 80%
    (1.24, 0.75, "CONDITIONAL"),
    (1.00, 0.75, "CONDITIONAL"),
    (0.99, 0.75, "LIKELY DECLINE"),
])
def test_rental_brrr_tiers(dscr, ltv, expected):
    assert approval_likelihood("Rental", min_dscr=dscr, ltv=ltv) == expected


# A user minimum of 1.30 moves both lines up
@pytest.mark.parametrize("dscr, expected", [
    (1.29, "LIKELY DECLINE"),
    (1.30, "STRONG"),
])
def test_tiers_follow_user_minimum(dscr, expected):
    assert approval_likelihood("Rental", min_dscr=dscr, ltv=0.75,
                               dscr_min=1.30) == expected


@pytest.mark.parametrize("hm_ltv, expected", [
    (0.75, "LIKELY"),
    (0.7501, "UNLIKELY"),
])
def test_flip_tiers(hm_ltv, expected):
    assert approval_likelihood("Flip", hm_ltv_on_arv=hm_ltv) == expected


def test_r02_lender_figures():
    # v2 showed NOI Y1 $11,696 and LIKELY DECLINE for R-02
    r = analyze_deal(**RENTAL["R-02"])
    assert r["loan_amount"] == pytest.approx(255000.00, abs=0.01)
    assert r["ltv"] == pytest.approx(0.75)
    assert r["noi_y1"] == pytest.approx(11696.00, abs=0.01)
    assert r["annual_debt_service"] == pytest.approx(19847.10, abs=0.01)
    assert approval_likelihood("Rental", r["min_dscr"], r["ltv"]) == "LIKELY DECLINE"


def test_f01a_fundability():
    # v2 showed LIKELY at 62.31% HM LTV on ARV for F-01a
    r = analyze_deal(**FLIP["F-01a"])
    hm_ltv_on_arv = r["hm_loan"] / FLIP["F-01a"]["arv"]
    assert hm_ltv_on_arv == pytest.approx(0.6231, abs=0.0001)
    assert approval_likelihood("Flip", hm_ltv_on_arv=hm_ltv_on_arv) == "LIKELY"