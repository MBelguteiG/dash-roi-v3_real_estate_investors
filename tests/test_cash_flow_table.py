import pytest
from engine.analyze import analyze_deal
from tests.test_regression_rental import CASES

R02 = CASES["R-02"]
R = analyze_deal(**R02)
T = R["cash_flow_table"]


def test_one_row_per_year():
    assert [r["year"] for r in T] == list(range(1, R02["exit_year"] + 1))


def test_year1_matches_lender_view():
    assert T[0]["noi"] == pytest.approx(R["noi_y1"])
    assert T[0]["interest"] + T[0]["principal"] == pytest.approx(R["annual_debt_service"])


def test_min_dscr_matches_tile():
    assert min(r["dscr"] for r in T) == pytest.approx(R["min_dscr"])


def test_rows_add_up():
    for r in T:
        assert r["effective_income"] - r["operating_expenses"] == pytest.approx(r["noi"])
        assert r["noi"] - r["interest"] - r["capex_reserve"] == pytest.approx(r["cash_flow"])


def test_sale_only_in_exit_year():
    assert all(r["sale_proceeds"] == 0 for r in T[:-1])
    assert T[-1]["sale_proceeds"] > 0