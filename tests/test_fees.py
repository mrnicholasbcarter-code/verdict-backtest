import pytest

from backtest_harness.fee_models import BoundedProfitFeeModel, FlatMakerTakerModel


class TestBoundedProfitFeeModel:
    def test_standard_fee(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
        assert model.calculate_fee(50.0, 100.0) == pytest.approx(3.5)

    def test_fee_capped_at_maximum(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
        assert model.calculate_fee(10.0, 100.0) == pytest.approx(5.0)

    def test_zero_fee_on_loss(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
        assert model.calculate_fee(100.0, 50.0) == pytest.approx(0.0)

    def test_zero_fee_on_breakeven(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
        assert model.calculate_fee(100.0, 100.0) == pytest.approx(0.0)

    def test_custom_percentage(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.10, maximum_fee_cents=100.0)
        assert model.calculate_fee(0.0, 100.0) == pytest.approx(10.0)

    def test_tiny_profit(self):
        model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=5.0)
        assert model.calculate_fee(99.0, 100.0) == pytest.approx(0.07)


class TestFlatMakerTakerModel:
    def test_maker_zero_fee(self):
        model = FlatMakerTakerModel(maker_bps=0.0, taker_bps=0.001)
        assert model.calculate_fee(1000.0, is_maker=True) == pytest.approx(0.0)

    def test_taker_fee(self):
        model = FlatMakerTakerModel(maker_bps=0.0, taker_bps=0.001)
        assert model.calculate_fee(1000.0, is_maker=False) == pytest.approx(1.0)

    def test_custom_maker_fee(self):
        model = FlatMakerTakerModel(maker_bps=0.0005, taker_bps=0.001)
        assert model.calculate_fee(10000.0, is_maker=True) == pytest.approx(5.0)
