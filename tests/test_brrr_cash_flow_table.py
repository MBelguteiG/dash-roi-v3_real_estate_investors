import pytest
from engine.analyze import analyze_deal
from tests.test_regression_brrr import B01

R = analyze_deal(**B01)
T = R["cash_flow_table"]


def test_one_row_per_year():
    assert [r["year"] for r in T] == list(range(1, B01["exit_year"] + 1))


def test_refi_cash_and_sale_land_once():
    assert sum(r["cash_out_at_refi"] for r in T) == pytest.approx(R["cash_pulled_out"])
    assert sum(r["sale_proceeds"] for r in T) == pytest.approx(R["net_sale_proceeds"])
    assert T[-1]["sale_proceeds"] > 0


def test_rows_add_up():
    for r in T:
        assert r["noi"] - r["capex_reserve"] - r["debt_service"] == pytest.approx(r["cash_flow"])


def test_sale_only_in_exit_year():
    assert all(r["sale_proceeds"] == 0 for r in T[:-1])