"""
BRRR: the property is empty during repairs (Nov 2026). Months 1..refi_month
earn no rent; you still pay property tax, insurance, HOA and the
short-term loan interest. Rent starts the month after the refinance.
rent_during_rehab=True keeps the v2 method for the v2 parity checks.
"""
import pytest
from engine.analyze import analyze_deal
from engine.brrr import build_brrr_monthly_stream
from tests.test_regression_brrr import B01

# BDash's IL condo check deal (2026-11-11), without points
CONDO = dict(model="BRRR", state="Illinois", property_type="Condo", scenario="Base",
             price=200000, rehab=25000, arv=300000, base_rent=2100, exit_year=4,
             target_irr=0.10, hm_ltv=0.80, hm_rate=0.12, refi_month=6,
             refi_ltv=0.75, post_refi_rate=0.0655, refi_type="Cash-Out")


def test_condo_irr_by_hand():
    # independent rebuild: 22.36% (it was 28.09%-style with rent from month 1)
    assert analyze_deal(**CONDO)["irr"] == pytest.approx(0.223607, abs=5e-6)


def test_empty_month_cash_flow_by_hand():
    # IL condo: tax 200,000 x 2% / 12 = 333.33; insurance 1,000 / 12 = 83.33;
    # HOA 250; short-term interest 160,000 x 12% / 12 = 1,600
    stream, rows = build_brrr_monthly_stream(
        purchase_price=200000, rehab=25000, hm_ltv=0.80, hm_rate=0.12, refi_ltv=0.75,
        refi_month=6, post_refi_rate=0.0655, arv=300000, appreciation_rate=0.03,
        exit_year=4, selling_pct=0.08, cash_invested_amt=72500, base_rent=2100,
        vacancy_rate=0.05, tax_rate=0.02, annual_insurance=1000, hoa=250,
        base_maint=2100 * 0.08, mgmt_rate=0.08, capex_rate=0.05, rent_growth=0.025,
        tax_growth=0.03, inflation=0.027, return_rows=True)
    carry = 200000 * 0.02 / 12 + 1000 / 12 + 250
    for m in range(1, 6):                   # months 1-5: costs only
        assert stream[m] == pytest.approx(-carry - 1600, abs=1e-9)
    assert rows[0]["noi"] == pytest.approx(-carry)
    assert rows[0]["capex_reserve"] == 0.0
    assert rows[6]["noi"] > 0               # month 7: rent has started


def test_rent_starts_after_the_refi_month():
    a = analyze_deal(**{**CONDO, "refi_month": 3})["irr"]
    b = analyze_deal(**{**CONDO, "refi_month": 9})["irr"]
    assert a > b                            # a longer empty period costs more


def test_empty_period_lowers_the_return():
    new = analyze_deal(**B01)["irr"]
    v2 = analyze_deal(**B01, rent_during_rehab=True)["irr"]
    assert new < v2


def test_v2_method_still_available():
    # B-01 under the v2 method matches the old locked value
    assert analyze_deal(**B01, rent_during_rehab=True)["irr"] == pytest.approx(0.06104, abs=0.00005)


def test_cash_and_dscr_unchanged():
    # the empty months don't touch the loans, the cash in, or the lender DSCR
    new = analyze_deal(**B01)
    v2 = analyze_deal(**B01, rent_during_rehab=True)
    for k in ("cash_invested", "cash_pulled_out", "cash_left", "dscr", "refi_loan"):
        assert new[k] == pytest.approx(v2[k])
