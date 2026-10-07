import pytest
from engine.analyze import analyze_deal

B01 = dict(model="BRRR", state="Illinois", property_type="SFH",
           scenario="Base", price=250000, rehab=45000, base_rent=2400,
           exit_year=5, target_irr=0.10, arv=340000, hm_ltv=0.90,
           hm_rate=0.105, refi_ltv=0.75, refi_month=6,
           post_refi_rate=0.0725)


@pytest.mark.parametrize("year", [7, 8, 9, 10])
def test_brrr_long_hold_does_not_crash(year):
    result = analyze_deal(**{**B01, "exit_year": year})
    assert -1 < result["irr"] < 1