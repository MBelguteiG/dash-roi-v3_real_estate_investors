import pytest
from tests.test_regression_rental import CASES
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out
from tests.test_regression_brrr import B01

TOL = 0.02  # dollars, same as crosscheck SOLVER_TOL

# (label, solver, case, expected price)
SOLVER_CASES = [
    # R-05: v2 recorded no figure, only that it solves below the 500K asking price
    ("R-05-irr-on-R-01", max_price_irr, "R-01", 297588.34),
    # R-06: rent / PITIA = 1.00 (Nov 2026; v2 used NOI / debt at 1.20)
    ("R-06-dscr-on-R-02", max_price_dscr, "R-02", 321000.01),
    # v2 showed 207,287.11
    ("irr-on-R-02", max_price_irr, "R-02", 207286.17),
    # rent / PITIA = 1.00 (Nov 2026)
    ("dscr-on-R-03", max_price_dscr, "R-03", 335930.24),
]
IDS = [c[0] for c in SOLVER_CASES]


@pytest.mark.parametrize("label, solver, case, expected", SOLVER_CASES, ids=IDS)
def test_rental_solver(label, solver, case, expected):
    result = solver(CASES[case])
    assert result["status"] == "SOLVED"
    assert result["price"] == pytest.approx(expected, abs=TOL)


def test_brrr_irr_solver_b05():
    # v2 recorded no figure, only that the solver gives a sensible price
    result = max_price_irr(B01)
    assert result["status"] == "SOLVED"
    assert result["price"] == pytest.approx(231069.01, abs=TOL)   # empty until the refi


def test_brrr_dscr_solver_refuses_b06():
    # v2 refuses too: post-refi DSCR is sized off ARV, not purchase price
    result = max_price_dscr(B01)
    assert result["status"] == "REFUSED"
    assert result["price"] is None


def test_brrr_all_cash_out_b01():
    # v2 B50 showed 200,475 (uses Flip costs at current price); v3 is exact
    result = max_price_all_cash_out(B01)
    assert result["status"] == "SOLVED"
    assert result["price"] == pytest.approx(202409.64, abs=TOL)