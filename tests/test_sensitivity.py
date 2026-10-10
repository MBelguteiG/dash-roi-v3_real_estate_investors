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


from engine.assumptions import get_assumptions

A = get_assumptions("Illinois", "SFH", "Rental", "Base")
BASE = analyze_deal(**DEAL)


def test_override_with_same_value_changes_nothing():
    same = {"Appreciation Annual": A["Appreciation Annual"]}
    r = analyze_deal(**DEAL, overrides=same)
    assert r["irr"] == pytest.approx(BASE["irr"], abs=1e-12)


def test_higher_appreciation_raises_irr():
    up = {"Appreciation Annual": A["Appreciation Annual"] + 0.01}
    assert analyze_deal(**DEAL, overrides=up)["irr"] > BASE["irr"]


def test_higher_vacancy_lowers_dscr():
    up = {"VacancyRate% Annual": A["VacancyRate% Annual"] + 0.05}
    assert analyze_deal(**DEAL, overrides=up)["min_dscr"] < BASE["min_dscr"]


def test_unknown_assumption_is_rejected():
    with pytest.raises(ValueError):
        analyze_deal(**DEAL, overrides={"Apreciation": 0.05})


def test_overrides_refused_outside_rental():
    from tests.test_regression_brrr import CASES as BRRR
    with pytest.raises(ValueError):
        analyze_deal(**BRRR["B-01"], overrides={"Appreciation Annual": 0.05})

from engine.sensitivity import tornado_irr

TORNADO = tornado_irr(DEAL)
BY_NAME = {r["variable"]: r for r in TORNADO["rows"]}


def test_tornado_has_seven_rows_and_base():
    assert len(TORNADO["rows"]) == 7
    assert TORNADO["base"] == pytest.approx(BASE["irr"], abs=1e-12)


def test_tornado_sorted_by_width():
    widths = [abs(r["high"] - r["low"]) for r in TORNADO["rows"]]
    assert widths == sorted(widths, reverse=True)


def test_tornado_directions():
    base = TORNADO["base"]
    assert BY_NAME["Purchase price"]["low"] > base > BY_NAME["Purchase price"]["high"]
    assert BY_NAME["Interest rate"]["low"] > base > BY_NAME["Interest rate"]["high"]
    assert BY_NAME["Monthly rent"]["low"] < base < BY_NAME["Monthly rent"]["high"]
    assert BY_NAME["Appreciation"]["low"] < base < BY_NAME["Appreciation"]["high"]
    assert BY_NAME["Vacancy rate"]["low"] > base > BY_NAME["Vacancy rate"]["high"]


def test_rate_bars_match_heatmap():
    # The tornado's rate swing (+/-1 point) equals the heatmap's outer rows
    assert BY_NAME["Interest rate"]["low"] == pytest.approx(GRID["irr"][0][2], abs=1e-12)
    assert BY_NAME["Interest rate"]["high"] == pytest.approx(GRID["irr"][4][2], abs=1e-12)


def test_zero_rehab_gives_zero_width():
    assert BY_NAME["Rehab cost"]["low"] == pytest.approx(BY_NAME["Rehab cost"]["high"])