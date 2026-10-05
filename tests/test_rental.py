import pytest
from engine.analyze import analyze_deal
from engine.crosscheck import DEALS, PCT


def test_rental_irr_documented():
    result = analyze_deal(**DEALS["Rental"])
    assert result["irr"] == pytest.approx(-0.0539, abs=PCT)