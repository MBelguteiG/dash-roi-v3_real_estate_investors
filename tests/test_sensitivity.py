import pytest
from engine.analyze import analyze_deal
from engine.sensitivity import two_way_irr
from tests.test_regression_rental import CASES

DEAL = CASES["R-02"]
GRID = two_way_irr(DEAL)


def test_grid_is_5_by_5():
    assert len(GRID["irr"]) == 5
    assert all(len(row) == 5 for row in GRID["irr"])


def test_axes_match_v2_steps():
    assert GRID["prices"] == pytest.approx([306000, 323000, 340000, 357000, 374000])
    assert GRID["rates"] == pytest.approx([0.0575, 0.0625, 0.0675, 0.0725, 0.0775])


def test_centre_cell_is_the_base_deal():
    base = analyze_deal(**DEAL)["irr"]
    assert GRID["irr"][2][2] == pytest.approx(base, abs=1e-12)


def test_irr_falls_as_price_rises():
    for row in GRID["irr"]:
        assert all(a > b for a, b in zip(row, row[1:]))


def test_irr_falls_as_rate_rises():
    for col in range(5):
        column = [row[col] for row in GRID["irr"]]
        assert all(a > b for a, b in zip(column, column[1:]))