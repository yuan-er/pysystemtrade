# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2021-08-02"

"""
generate order for backtrader
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
    use_fix_strategy_weight = True
    use_fix_instrument_weight = False

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
    my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16))
    # my_rules = Rules(dict(ewmac4=ewmac_4, ewmac8=ewmac_8))

    my_config = Config()
    my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16)
    # my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8)
    # from config.etf_test_portfolio_cfg import etf_instruments
    # print(etf_instruments.keys())
    # exit()
    instrument_dict = {'159929': 1100, '510050': 1200, '159949': 1600, '510330': 800, '510500': 700, '588000': 1900,
                       '501077': 1400, '161912': 1100, '501046': 1200, '162720': 3800, '160529': 3700, '506002': 2900,
                       '506005': 3800, '501093': 2000, '501062': 4400, '168207': 4200, '501085': 1800, '506001': 2700,
                       '501078': 1500, '163417': 2300, '161005': 1400, '513050': 1300, '512800': 4200, '159928': 100,
                       '512000': 3500, '512200': 5900, '512580': 1300, '512660': 1900, '161631': 2800, '512400': 1300,
                       '512690': 1100, '159995': 1100, '515790': 1000, '515030': 700, '516780': 1300, '515170': 3200,
                       '515220': 1300, '515210': 1100, '159825': 4800, '513100': 1400, '513500': 4200, '513080': 6900,
                       '513030': 7600, '513520': 6400, '510900': 2900, '518880': 100, '160416': 4200, '162411': 6200,
                       '160723': 3600, '501018': 4000, '511260': 100, '511010': 100}

    instruments = []
    # codes =  ['510050.sh', '159949.sz', '510330.sh', '510500.sh', '588000.sh',
    #                       '501077.sh', '161912.sz',  #'501046.sh',
    #                       '163417.sz', '161005.sz',
    #                       '513050.sh',
    #                       '513100.sh', '513500.sh',
    #                       '518880.sh', '160416.sz']
    # codes = ['510050.sh', '510330.sh', '510500.sh', '501077.sh', '161912.sz', '168207.sz', '501085.sh', '506001.sh',
    #          '501078.sh', '513050.sh', '513100.sh', '513500.sh', '518880.sh', '162411.sz', '511260.sh']
    codes = ['510050.sh', '510330.sh', '510500.sh', '501077.sh', '161912.sz', '168207.sz', '501085.sh', '501078.sh', '513050.sh', '513100.sh', '513500.sh', '518880.sh', '162411.sz', '511260.sh']
    for code in codes:
        instruments.append(code.split('.')[0])

    # instrument_dict.pop('511260')
    # instrument_dict.pop('511010')
    my_config.instruments = instruments
    # my_config.instruments = ['510050', '159949', '510330', '510500','588000', '513050', '513100', '513500', '518880', '160416']
    my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3, ewmac16=3.75)
    # my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3)
    my_config.use_forecast_scale_estimates = False
    # my_config.use_forecast_scale_estimates = True

    fcs = ForecastScaleCap()

    my_account = Account()
    combiner = ForecastCombine()
    raw_data = RawData()
    position_size = PositionSizing()

    if not use_fix_strategy_weight:
        my_config.forecast_weight_estimate = dict(method="shrinkage")
        my_config.use_forecast_weight_estimates = True
        my_config.use_forecast_div_mult_estimates = True
    else:
        my_config.forecast_weights = dict(ewmac4=0.42, ewmac8=0.16, ewmac16=0.42)
        # my_config.forecast_weights = dict(ewmac4=0.5, ewmac8=0.5)
        my_config.forecast_div_multiplier = 1.12
        my_config.use_forecast_weight_estimates = False
        my_config.use_forecast_div_mult_estimates = False

    # size positions
    possizer = PositionSizing()
    my_config.percentage_vol_target = 20
    my_config.notional_trading_capital = 300000
    my_config.base_currency = "USD"

    # portfolio - estimated
    portfolio = Portfolios()
    if not use_fix_instrument_weight:
        my_config.use_instrument_weight_estimates = True
        my_config.use_instrument_div_mult_estimates = True
        my_config.instrument_weight_estimate = dict(
            method="shrinkage", date_method="expanding")
    else:
        my_config.use_instrument_weight_estimates = False
        my_config.use_instrument_div_mult_estimates = False
        # my_config.instrument_weights = {'159949': 0.067071, '510050': 0.031397, '510330': 0.029435, '510500': 0.063739,
        #                                 '588000': 0.06, '501077': 0.116602, '161912': 0.14487, '163417': 0.063142,
        #                                 '161005': 0.065914, '513050': 0.065625, '513100': 0.075418, '513500': 0.060096,
        #                                 '518880': 0.068981, '160416': 0.08771}

        my_config.instrument_weights = {'161912': 0.10476973290321802, '162411': 0.03568487505941734,
                                        '168207': 0.059009398327644433,
                                        '501077': 0.087258733744876394, '501078': 0.09872085803951536,
                                        '501085': 0.07604016550026339,
                                        '506001': 0.05025289016727335, '510050': 0.08046374862775303,
                                        '510330': 0.0509247100244872,
                                        '510500': 0.04978564418937405, '511260': 0.034467881893424306,
                                        '513050': 0.061096279362027786,
                                        '513100': 0.07420791242200993, '513500': 0.08914908212154771,
                                        '518880': 0.04816808761716694}

        my_config.instrument_div_multiplier = 1.12

    my_config.forecast_floor = 0
    my_system = System(
        [fcs, my_rules, combiner, possizer, portfolio, my_account, raw_data], data, my_config
    )
    my_system.set_logging_level("on")
    profits = my_system.accounts.portfolio()
    print(profits.percent.stats())
    print(my_system.accounts.get_notional_capital())
    profits.curve().plot()
    from matplotlib.pyplot import show

    show()

    print(profits.gross.percent.stats())
    print(profits.net.percent.stats())

    instruments_weight_df = my_system.portfolio.get_instrument_weights()
    idm_df = my_system.portfolio.get_instrument_diversification_multiplier()
    # print(idm_df)
    # print(my_system.combForecast.get_combined_forecast())
    # print(my_system.positionSize.get_volatility_scalar())
    forecast_combine_df = pd.DataFrame()
    volatility_combine_df = pd.DataFrame()

    for code in my_config.instruments:
        code_forecast = my_system.combForecast.get_combined_forecast(code)
        volatility_scalar = my_system.positionSize.get_volatility_scalar(code)
        forecast_combine_df = forecast_combine_df.append(code_forecast, ignore_index=True)
        volatility_combine_df = volatility_combine_df.append(volatility_scalar, ignore_index=True)
        # print(code)
        # print(my_system.accounts.get_actual_position(code).tail(5))

    # print(my_system.forecastScaleCap.get_capped_forecast("159949", "ewmac4").tail(5))
    # print(my_system.rawdata.daily_returns_volatility("159949").tail(5))
    # print(my_system.forecastScaleCap.get_raw_forecast("159949", "ewmac4").tail(5))
    forecast_combine_df = forecast_combine_df.T
    forecast_combine_df.columns = my_config.instruments
    volatility_combine_df = volatility_combine_df.T
    volatility_combine_df.columns = my_config.instruments
    instruments_weight_df.to_csv('weight.csv')
    idm_df.to_csv('idm.csv')
    forecast_combine_df.to_csv('forecast.csv')
    volatility_combine_df.to_csv('vol.csv')
    print(my_system.portfolio.get_instrument_weights().tail(1).to_dict(orient='records'))
