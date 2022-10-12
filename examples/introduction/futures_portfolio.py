# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2022-08-02"

"""
查验pysys中期货的收益，以确定trading sys是否应该复现其效果
"""
import pandas as pd
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.example.rules import ewmac_forecast_with_defaults as ewmac
from systems.forecasting import Rules
from systems.trading_rules import TradingRule
from systems.basesystem import System
from sysdata.config.configdata import Config
from systems.forecast_scale_cap import ForecastScaleCap
from systems.forecast_combine import ForecastCombine
from systems.accounts.accounts_stage import Account
from systems.futures.rawdata import RawData
from systems.positionsizing import PositionSizing
from systems.portfolio import Portfolios


if __name__ == '__main__':

    data = csvFuturesSimData()

    ewmac_4 = TradingRule((ewmac, [], dict(Lfast=4, Lslow=16)))
    ewmac_8 = TradingRule(
        dict(
            function=ewmac,
            other_args=dict(
                Lfast=8,
                Lslow=32)))
    ewmac_16 = TradingRule(
        dict(
            function=ewmac,
            other_args=dict(
                Lfast=16,
                Lslow=64)))
    ewmac_32 = TradingRule(
        dict(
            function=ewmac,
            other_args=dict(
                Lfast=32,
                Lslow=128)))
    # my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16, ewmac32=ewmac_32))
    my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16))
    # my_rules = Rules(dict(ewmac8=ewmac_8, ewmac16=ewmac_16))

    my_config = Config()
    # my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16, ewmac32=ewmac_32)
    # my_config.trading_rules = dict(ewmac8=ewmac_8, ewmac16=ewmac_16)

    # we can estimate these ourselves
    my_config.instruments = ['HC', 'SP', 'AL', 'RB', 'EB']
    # my_config.instruments = [ 'IC']
    my_config.start_date = '2015-01-01'

    # my_config.instruments = select_dict.keys()
    # # my_config.instruments = get_etf_instruments()
    # exit()
    # my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3, ewmac16=3.75)
    # my_config.use_forecast_scale_estimates = False
    my_config.use_forecast_scale_estimates = True

    fcs = ForecastScaleCap()

    """
    combine some rules
    """
    # estimates:
    my_account = Account()
    combiner = ForecastCombine()
    raw_data = RawData()
    position_size = PositionSizing()

    my_config.forecast_weight_estimate = dict(method="shrinkage")
    my_config.use_forecast_weight_estimates = True
    my_config.use_forecast_div_mult_estimates = True

    # 使用固定预测权重
    # my_config.forecast_weights = dict(ewmac4=0.42, ewmac8=0.16, ewmac16=0.42)
    # my_config.forecast_div_multiplier = 1.12
    # my_config.use_forecast_weight_estimates = False
    # my_config.use_forecast_div_mult_estimates = False


    # size positions
    possizer = PositionSizing()
    my_config.percentage_vol_target = 20
    my_config.notional_trading_capital = 500000
    my_config.base_currency = "USD"

    # portfolio - estimated
    portfolio = Portfolios()
    my_config.use_instrument_weight_estimates = True
    my_config.use_instrument_div_mult_estimates = True
    my_config.instrument_weight_estimate = dict(
        method="shrinkage", date_method="expanding")

    """
    Have we made some dosh?
    """
    # print(my_config.start_date)
    # exit()
    # my_config.forecast_floor=0
    my_system = System(
        [fcs, my_rules, combiner, possizer, portfolio, my_account, raw_data], data, my_config
    )
    my_system.set_logging_level("on")
    # pd.set_option("max_columns", None)
    # pd.set_option("max_rows", None)

    print(my_system.forecastScaleCap.get_forecast_cap())

    profits = my_system.accounts.portfolio()

    print(profits.percent.stats())
    print(my_system.accounts.get_notional_capital())
    # print(profits.curve().tail(60))
    profits.curve().plot()
    from matplotlib.pyplot import show
    show()

    # have costs data now
    print(profits.gross.percent.stats())
    print(profits.net.percent.stats())
    print(my_system.accounts.portfolio().annual)
    my_system.accounts.portfolio().drawdown().plot()
    show()

    # print(my_system.positionSize.get_price_volatility("HC").tail(5))
    # print(my_system.positionSize.get_block_value("HC").tail(5))
    # print(my_system.positionSize.get_underlying_price("HC"))
    # print(my_system.positionSize.get_instrument_value_vol("HC").tail(5))
    # print(my_system.positionSize.get_volatility_scalar("HC").tail(5))
    # print(my_system.positionSize.get_vol_target_dict())
    # print(my_system.positionSize.get_subsystem_position("HC").tail(5))

    print('instrument weight: ')
    my_system.portfolio.get_instrument_weights().to_csv('weight.csv')
    print(my_system.portfolio.get_instrument_weights().tail(10))

    # print(my_system.portfolio.get_instrument_weights().head(1).to_dict(orient='records'))
    #
    # print(my_system.portfolio.get_instrument_weights().tail(1).to_dict(orient='records'))
    #
    my_system.portfolio.get_instrument_diversification_multiplier().to_csv('mul.csv')
    print(my_system.portfolio.get_instrument_diversification_multiplier().tail(5))
    for code in my_config.instruments:
        print(code)
        print(my_system.combForecast.get_combined_forecast(code).tail(5))
        # print(my_system.positionSize.get_volatility_scalar(code).tail(5))
        # print(my_system.positionSize.get_vol_target_dict())

        # print(my_system.positionSize.get_subsystem_position(code).tail(5)) # 子系统仓位
        # print(my_system.portfolio.get_notional_position(code).tail(10)) # 最终系统仓位
        print(my_system.accounts.get_actual_position(code).tail(10))
