import pytest
from backtest_harness.fee_models import BoundedProfitFeeModel

def test_bounded_profit_fee():
    model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
    
    # Gross profit = 50, fee = 3.5
    assert model.calculate_fee(50.0, 100.0) == pytest.approx(3.5)
    
    # Gross profit = 90, fee = 6.3 -> capped at 5.0
    assert model.calculate_fee(10.0, 100.0) == pytest.approx(5.0)
    
    # Loss, fee = 0
    assert model.calculate_fee(50.0, 0.0) == pytest.approx(0.0)
