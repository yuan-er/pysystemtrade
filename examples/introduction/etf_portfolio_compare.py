# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2021-07-27"

"""
验证etf组合是否与backtrader计算结果一致
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

from config.etf_compare_portfolio_cfg import etf_instruments


def get_etf_instruments():
    instruments = []
    for code in etf_instruments.keys():
        instruments.append(code.split('.')[0])
        print(code.split('.')[0]+ ',100,Equity,USD,0,0,0.00025,5,ETF')
    return instruments

# def get_etf_instruments():
#     instruments = []
#     for code in etf_instruments.keys():
#         instruments.append(code.split('.')[0])
#         print(code.split('.')[0]+ ',100.0,5.0,Equity,0.0,ETF,0.00025,USD,0.0')
#     return instruments

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
    ewmac_64 = TradingRule(
        dict(
            function=ewmac,
            other_args=dict(
                Lfast=64,
                Lslow=256)))

    my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16, ewmac32=ewmac_32, ewmac64=ewmac_64))
    # my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16))
    # my_rules = Rules(dict(ewmac8=ewmac_8, ewmac16=ewmac_16))

    my_config = Config()
    # my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16, ewmac32=ewmac_32)
    # my_config.trading_rules = dict(ewmac8=ewmac_8, ewmac16=ewmac_16)

    # we can estimate these ourselves
    # my_config.instruments = ['159949', '510050', '510330', '501077', '161912', '501046',
    #                          '163417', '161005', '513050', '513100', '513500', '518880', '160416']
    # my_config.start_date = '2020-01-01'
    # select_dict = {'159825': 22.6, '162411': 33.0, '512660': 7.7, '513100': 9.5, '518880': 15.4, '515210': 9.0, '512800': 22.2, '511260': 2.3, '160723': 22.1, '513520': 42.9, '512690': 6.3, '513500': 25.9, '159995': 5.2, '513030': 42.0, '515220': 10.9, '511010': 2.8, '501018': 23.8, '513080': 39.1, '510900': 18.3, '515170': 13.4, '501093': 8.0, '588000': 5.5, '515790': 3.7, '160416': 24.8, '512000': 14.5, '515030': 2.9, '513050': 8.9, '510500': 5.0, '161912': 8.8, '159949': 5.6, '161631': 8.7, '159929': 4.4, '512580': 5.4, '501077': 4.9, '163417': 14.7, '512200': 22.2, '510330': 1.8, '512400': 5.9, '161005': 5.9, '510050': 2.4}

    # print(len(select_dict.keys()))

    # my_config.instruments = select_dict.keys()
    my_config.instruments = get_etf_instruments()

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

    # size positions
    possizer = PositionSizing()
    my_config.percentage_vol_target = 20
    my_config.notional_trading_capital = 300000
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
    my_config.forecast_floor=0
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
    profits.curve().plot()
    from matplotlib.pyplot import show
    show()

    # have costs data now
    print(profits.gross.percent.stats())
    print(profits.net.percent.stats())

    print(my_system.portfolio.get_instrument_weights().tail(5))

    print(my_system.portfolio.get_instrument_weights().head(1).to_dict(orient='records'))

    print(my_system.portfolio.get_instrument_weights().tail(1).to_dict(orient='records'))

    print(my_system.portfolio.get_instrument_diversification_multiplier().tail(5))
    for code in my_config.instruments:
        print(code)
        print(my_system.combForecast.get_combined_forecast(code).tail(5))

        print(my_system.positionSize.get_volatility_scalar(code).tail(5))
        print(my_system.positionSize.get_vol_target_dict())

        # print(my_system.positionSize.get_subsystem_position(code).tail(5)) # 子系统仓位
        print(my_system.portfolio.get_notional_position(code).tail(2)) # 最终系统仓位
        # print(my_system.accounts.get_actual_position(code).tail(5))
