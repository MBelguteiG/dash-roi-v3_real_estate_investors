import pytest
from engine.analyze import analyze_deal
from engine.brrr import rate_term_ltv
from tests.test_regression_brrr import B01

CASH = analyze_deal(**B01)
RT = analyze_deal(**B01, refi_type="Rate/Term")


def test_rate_term_ltv_caps_at_hm_payoff():
    # B-01: HM loan 225,000 on ARV 340,000, under the 75% cap
    assert rate_term_ltv(340000, 0.75, 250000, 0.90) == pytest.approx(225000 / 340000)


def test_rate_term_ltv_never_exceeds_refi_ltv():
    assert rate_term_ltv(340000, 0.60, 250000, 0.90) == pytest.approx(0.60)


def test_cash_out_is_still_the_default():
    assert CASH["refi_type"] == "Cash-Out"
    assert CASH["refi_loan"] == pytest.approx(255000.00)


def test_rate_term_pulls_no_cash():
    assert RT["refi_loan"] == pytest.approx(225000.00)
    assert RT["cash_pulled_out"] == pytest.approx(0.0, abs=0.01)
    assert RT["cash_left"] == pytest.approx(RT["cash_invested"], abs=0.01)


def test_rate_term_dscr_scales_with_smaller_loan():
    # Same NOI, same rate and term: DSCR is inverse to the loan amount
    assert RT["dscr"] == pytest.approx(CASH["dscr"] * 255000 / 225000, rel=1e-9)


def test_identical_when_cap_binds_below_payoff():
    # At 60% LTV the cap (204,000) is below the payoff, so both types match
    low = {**B01, "refi_ltv": 0.60}
    a = analyze_deal(**low)
    b = analyze_deal(**low, refi_type="Rate/Term")
    assert a["irr"] == pytest.approx(b["irr"], abs=1e-12)


def test_unknown_refi_type_rejected():
    with pytest.raises(ValueError):
        analyze_deal(**B01, refi_type="Cash-in")


from engine.solvers import max_price_irr, max_price_all_cash_out

RT_DEAL = {**B01, "refi_type": "Rate/Term"}


def test_all_cash_out_refused_for_rate_term():
    r = max_price_all_cash_out(RT_DEAL)
    assert r["status"] == "REFUSED"
    assert r["price"] is None


def test_all_cash_out_unchanged_for_cash_out():
    assert max_price_all_cash_out(B01)["price"] == pytest.approx(202409.64, abs=0.02)


def test_irr_solver_rate_term():
    r = max_price_irr(RT_DEAL)
    assert r["status"] == "SOLVED"
    assert r["price"] == pytest.approx(236540.70, abs=0.02)
    at_price = analyze_deal(**{**RT_DEAL, "price": r["price"]})
    assert at_price["irr"] == pytest.approx(0.10, abs=1e-6)