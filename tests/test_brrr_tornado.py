import pytest
from engine.analyze import analyze_deal
from engine.sensitivity import brrr_tornado_irr
from tests.test_regression_brrr import B01

TOR = brrr_tornado_irr(B01)
BY = {r["variable"]: r for r in TOR["rows"]}


def test_six_rows_and_base():
    assert len(TOR["rows"]) == 6
    assert TOR["base"] == pytest.approx(analyze_deal(**B01)["irr"], abs=1e-12)
    assert TOR["base_all_cash_out"] is False


def test_sorted_by_width():
    widths = [abs(r["high"] - r["low"]) for r in TOR["rows"]]
    assert widths == sorted(widths, reverse=True)


def test_directions():
    base = TOR["base"]
    assert BY["ARV"]["low"] < base < BY["ARV"]["high"]
    assert BY["Monthly rent"]["low"] < base < BY["Monthly rent"]["high"]
    assert BY["Post-refi rate"]["low"] > base > BY["Post-refi rate"]["high"]
    assert BY["Purchase price"]["low"] > base > BY["Purchase price"]["high"]


def test_no_all_cash_out_at_b01_swings():
    # ARV +10% pulls 55,500 vs 79,375 invested; refi LTV 80% pulls 47,000
    assert not any(r["all_cash_out"] for r in TOR["rows"])


def test_rate_term_deal_runs():
    rt = brrr_tornado_irr({**B01, "refi_type": "Rate/Term"})
    assert len(rt["rows"]) == 6