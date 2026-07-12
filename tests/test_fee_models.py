from backtest_harness.fee_models import BoundedProfitFeeModel, FlatMakerTakerModel


def test_bounded_profit_fee_caps_positive_profit() -> None:
    model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=0.05)

    assert model.calculate_fee(entry_cents=40.0, payout_cents=100.0) == 0.05


def test_bounded_profit_fee_is_zero_when_trade_loses() -> None:
    model = BoundedProfitFeeModel(percent_of_profit=0.07, maximum_fee_cents=0.05)

    assert model.calculate_fee(entry_cents=100.0, payout_cents=40.0) == 0.0


def test_flat_maker_taker_uses_correct_rate() -> None:
    model = FlatMakerTakerModel(maker_bps=0.0002, taker_bps=0.001)

    assert model.calculate_fee(trade_volume=1_000.0, is_maker=True) == 0.2
    assert model.calculate_fee(trade_volume=1_000.0, is_maker=False) == 1.0
