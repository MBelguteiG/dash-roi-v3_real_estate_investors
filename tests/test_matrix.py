import math
import pytest
from engine.analyze import analyze_deal
from tests.test_regression_rental import CASES as RENTAL
from tests.test_regression_brrr import B01
from tests.test_regression_flip import CASES as FLIP

BASES = {"Rental": RENTAL["R-02"], "BRRR": B01, "Flip": FLIP["F-02a"]}
STATES = ["Illinois", "California"]
TYPES = ["SFH", "Condo", "Townhouse", "Duplex"]
SCENARIOS = ["Conservative", "Base", "Aggressive"]
VERDICTS = {"STRONG BUY", "BUY", "NEGOTIATE", "REJECT", "HARD REJECT"}

COMBOS = [(m, s, t, sc) for m in BASES for s in STATES for t in TYPES for sc in SCENARIOS]


def finite(x):
    return x is None or (isinstance(x, (int, float)) and math.isfinite(x))


@pytest.mark.parametrize("model, state, ptype, scenario", COMBOS,
                         ids=[f"{m}-{s[:2]}-{t}-{sc[:4]}" for m, s, t, sc in COMBOS])
def test_every_combination_runs(model, state, ptype, scenario):
    deal = {**BASES[model], "state": state, "property_type": ptype, "scenario": scenario}
    r = analyze_deal(**deal)
    assert r["verdict"] in VERDICTS
    for key, value in r.items():
        if isinstance(value, float):
            assert finite(value), f"{key} = {value}"


@pytest.mark.parametrize("model", ["Rental", "BRRR"])
@pytest.mark.parametrize("year", [1, 2, 3, 10, 15, 20, 25, 30])
def test_hold_periods(model, year):
    r = analyze_deal(**{**BASES[model], "exit_year": year})
    assert -1 < r["irr"] < 10
    assert r["verdict"] in VERDICTS