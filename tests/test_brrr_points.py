import pytest
from engine.analyze import analyze_deal
from engine.amortization import annual_debt_service

B = dict(model="BRRR", state="California", property_type="Townhouse",
         scenario="Base", price=650000, rehab=25000, base_rent=4500,
         exit_year=5, target_irr=0.13, arv=800000, hm_ltv=0.85,
         hm_rate=0.12, refi_ltv=0.75, refi_month=6, post_refi_rate=0.09)
BASE = analyze_deal(**B)
ONE = analyze_deal(**B, points=1.0)


def test_zero_points_changes_nothing():
    r = analyze_deal(**B, points=0.0)
    for key in ("irr", "dscr", "cash_left", "required_rent", "real_irr"):
        assert r[key] == pytest.approx(BASE[key], abs=1e-12)


def test_one_point_cost_and_rate():
    assert ONE["points_cost"] == pytest.approx(6000.00)        # 1% of the $600,000 new loan
    assert ONE["rate_used"] == pytest.approx(0.09 - 0.0025)


def test_saving_and_breakeven():
    saving = (annual_debt_service(600000, 0.09)
              - annual_debt_service(600000, 0.0875)) / 12
    assert ONE["monthly_saving"] == pytest.approx(saving)
    assert ONE["breakeven_months"] == pytest.approx(6000 / saving)


def test_points_raise_dscr_and_cash_left():
    assert ONE["dscr"] > BASE["dscr"]
    assert ONE["cash_left"] == pytest.approx(BASE["cash_left"] + 6000)


@pytest.mark.parametrize("r", [BASE, ONE])
def test_table_cash_back_matches(r):
    table_total = sum(row["cash_out_at_refi"] for row in r["cash_flow_table"])
    assert table_total == pytest.approx(r["cash_pulled_out"])


def test_negative_points_rejected():
    with pytest.raises(ValueError):
        analyze_deal(**B, points=-1)