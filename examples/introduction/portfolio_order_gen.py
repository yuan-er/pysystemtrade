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

    my_config = Config()
    my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16)
    # from config.etf_test_portfolio_cfg import etf_instruments
    # print(etf_instruments.keys())
    # exit()
    instruments = ['510050.sh', '159949.sz', '510330.sh', '510500.sh', '588000.sh', '501077.sh', '161912.sz',
                   '162720.sz', '513100.sh', '513500.sh',
                   '513030.sh', '513520.sh', '510900.sh', '518880.sh', '162411.sz',
                   '511260.sh', '511010.sh']

    codes = []
    for code in instruments:
        codes.append(code.split('.')[0])
        print(code.split('.')[0] + ',100,Equity,USD,0,0,0.00005,0,ETF')

    my_config.instruments = codes
    my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3, ewmac16=3.75)
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
        my_config.instrument_weights = dict()
        my_config.instrument_div_multiplier = 1.12

    my_config.forecast_floor = 0
    my_system = System(
        [fcs, my_rules, combiner, possizer, portfolio, my_account, raw_data], data, my_config
    )
    my_system.set_logging_level("on")
    profits = my_system.accounts.portfolio()

    instruments_weight_df = my_system.portfolio.get_instrument_weights()
    idm_df = my_system.portfolio.get_instrument_diversification_multiplier()

    # print(my_system.combForecast.get_combined_forecast())
    # print(my_system.positionSize.get_volatility_scalar())
    forecast_combine_df = pd.DataFrame()
    volatility_combine_df = pd.DataFrame()

    for code in my_config.instruments:
        code_forecast = my_system.combForecast.get_combined_forecast(code)
        volatility_scalar = my_system.positionSize.get_volatility_scalar(code)
        forecast_combine_df = forecast_combine_df.append(code_forecast, ignore_index=True)
        volatility_combine_df = volatility_combine_df.append(volatility_scalar, ignore_index=True)

    forecast_combine_df = forecast_combine_df.T
    forecast_combine_df.columns = my_config.instruments
    volatility_combine_df = volatility_combine_df.T
    volatility_combine_df.columns = my_config.instruments
    instruments_weight_df.to_csv('weight.csv')
    idm_df.to_csv('idm.csv')
    forecast_combine_df.to_csv('forecast.csv')
    volatility_combine_df.to_csv('vol.csv')
