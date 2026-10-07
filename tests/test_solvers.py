import pytest
from engine.crosscheck import SOLVER_CHECKS, SOLVER_TOL

IDS = [" ".join(c[0].split()) for c in SOLVER_CHECKS]


@pytest.mark.parametrize(
    "label, call, exp_status, exp_price, pass_label, note",
    SOLVER_CHECKS, ids=IDS)
def test_solver_check(label, call, exp_status, exp_price, pass_label, note):
    r = call()
    assert r["status"] == exp_status
    if exp_price is not None:
        assert abs(r["price"] - exp_price) <= SOLVER_TOL