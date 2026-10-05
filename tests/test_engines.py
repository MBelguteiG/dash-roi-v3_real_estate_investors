import pytest
from engine.analyze import analyze_deal
from engine.crosscheck import DEALS, CHECKS, close

RESULTS = {m: analyze_deal(**inputs) for m, inputs in DEALS.items()}
IDS = [f"{c[0]}-{c[1]}" for c in CHECKS]


@pytest.mark.parametrize("model, key, v2, v3_doc, tol, reason", CHECKS, ids=IDS)
def test_engine_check(model, key, v2, v3_doc, tol, reason):
    actual = RESULTS[model][key]
    expected = v2 if v3_doc is None else v3_doc
    assert close(actual, expected, tol), f"{model} {key}: got {actual}, expected {expected}"