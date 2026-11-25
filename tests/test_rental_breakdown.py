"""Rental cost breakdown (Nov 25, 2026). BDash's IL townhouse, Conservative,
$280,000, 20% down, 7.9% with 3 points, $2,500 rent, 4 years. Hand-checked:
rent 30,000; vacancy 6% 1,800; tax 2.1% 5,880; insurance 1,900; HOA 2,400;
maintenance 9% 2,700; management 8% 2,400 -> NOI 12,920; loan 18,154.93;
repairs 7% 2,100 -> -7,334.93. Sale 280,000 x 1.02^4 = 303,081 - 8% 24,246.48
- balance 214,129.10 = 64,705.43."""
import pytest
from engine.analyze import analyze_deal

R = analyze_deal(model="Rental", state="Illinois", property_type="Townhouse",
                 scenario="Conservative", price=280000, down_pct=0.20, annual_rate=0.079,
                 rehab=0, base_rent=2500, exit_year=4, target_irr=0.10, points=3)
Y1, LAST = R["cash_flow_table"][0], R["cash_flow_table"][-1]


@pytest.mark.parametrize("key, expected", [
    ("gross_rent", 30000), ("vacancy", 1800), ("tax", 5880), ("insurance", 1900),
    ("hoa", 2400), ("maintenance", 2700), ("management", 2400), ("noi", 12920),
    ("debt_service", 18154.93), ("capex_reserve", 2100), ("cash_flow", -7334.93)])
def test_year1_by_hand(key, expected):
    assert Y1[key] == pytest.approx(expected, abs=0.01)


def test_sale_by_hand():
    assert LAST["sale_price"] == pytest.approx(303081.00, abs=0.01)
    assert LAST["selling_cost"] == pytest.approx(24246.48, abs=0.01)
    assert LAST["loan_balance"] == pytest.approx(214129.10, abs=0.01)
    assert LAST["sale_price"] - LAST["selling_cost"] - LAST["loan_balance"] \
        == pytest.approx(LAST["sale_proceeds"])


def test_every_year_adds_up():
    for y in R["cash_flow_table"]:
        costs = y["vacancy"] + y["tax"] + y["insurance"] + y["hoa"] + y["maintenance"] + y["management"]
        assert y["gross_rent"] - costs == pytest.approx(y["noi"])


def test_cash_in_by_hand():
    assert R["down_payment"] + R["closing_costs"] + R["points_cost"] == pytest.approx(73220)
    assert R["cash_in"] == pytest.approx(73220)
