"""BRRR refinance closing costs (Nov 19, 2026).
Freddie Mac: 3%-6% of the new loan principal. By scenario: Conservative 6%,
Base 4.5%, Aggressive 3%. Paid out of the cash at the refinance.
BDash's IL townhouse deal. The Base IRR 7.3789% was hand-checked with scipy
brentq on the unchanged monthly stream minus $10,968.75 in month 6."""
import pytest
from engine.analyze import analyze_deal

DEAL = dict(model="BRRR", state="Illinois", property_type="Townhouse", scenario="Base",
            price=240000, rehab=25000, arv=325000, base_rent=2800, exit_year=5,
            target_irr=0.10, hm_ltv=0.80, hm_rate=0.12, refi_month=6, refi_ltv=0.75,
            post_refi_rate=0.078, refi_type="Cash-Out")


@pytest.mark.parametrize("scenario, pct", [("Conservative", 0.06), ("Base", 0.045),
                                           ("Aggressive", 0.03)])
def test_refi_cost_by_scenario(scenario, pct):
    r = analyze_deal(**{**DEAL, "scenario": scenario})
    assert r["refi_cost_pct"] == pytest.approx(pct)
    assert r["refi_cost"] == pytest.approx(243750 * pct)
    assert r["cash_pulled_out"] == pytest.approx(51750 - 243750 * pct)
    assert r["cash_left"] == pytest.approx(82000 - (51750 - 243750 * pct))


def test_base_irr_by_hand():
    assert analyze_deal(**DEAL)["irr"] == pytest.approx(0.0737890, abs=5e-7)


def test_without_refi_costs_matches_before():
    r = analyze_deal(**DEAL, refi_closing=False)
    assert r["cash_pulled_out"] == pytest.approx(51750)
    assert r["irr"] == pytest.approx(0.1087985, abs=5e-7)


def test_lender_fees_stay_apr_only():
    a = analyze_deal(**DEAL)
    b = analyze_deal(**DEAL, lender_fees=2000)
    assert a["irr"] == b["irr"] and a["cash_left"] == b["cash_left"]
