# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2021-07-27"

"""
判断etf是否应该加入组合
"""
from config.etf_test_portfolio_cfg import etf_instruments
from copy import copy

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
from sysquant.optimisation.optimisers.handcraft import *
from sysquant.estimators.estimates import Estimates, meanEstimates, stdevEstimates
from sysquant.optimisation.shared import neg_SR
from syscore.dateutils import WEEKS_IN_YEAR


def get_etf_instruments():
    instruments = []
    for code in etf_instruments.keys():
        instruments.append(code.split('.')[0])
        # print(code.split('.')[0]+ ',100,Equity,USD,0,0,0.00025,0,ETF')
    return instruments


def net_SR_for_instrument_in_system(system, instrument_code, instrument_weight_idm=0.25):
    maximum_pos_final = calculate_maximum_position(system, instrument_code, instrument_weight_idm=instrument_weight_idm)
    trading_cost = calculate_trading_cost(system, instrument_code)

    return net_SR_for_instrument(maximum_position=maximum_pos_final,
                                 trading_cost=trading_cost)


def calculate_maximum_position(system, instrument_code,
                               instrument_weight_idm=0.25
                               ):
    if instrument_weight_idm == 0:
        return 0.0

    if instrument_weight_idm > minimum_instrument_weight_idm:
        instrument_weight_idm = copy(minimum_instrument_weight_idm)
    pos_at_average = system.positionSize.get_volatility_scalar(instrument_code)
    pos_at_average_in_system = pos_at_average * instrument_weight_idm
    forecast_multiplier = system.combForecast.get_forecast_cap() / system.positionSize.avg_abs_forecast()

    maximum_pos_final = pos_at_average_in_system.iloc[-1] * forecast_multiplier

    return maximum_pos_final


def calculate_trading_cost(system, instrument_code):
    turnover = system.accounts.subsystem_turnover(instrument_code)
    SR_cost_per_trade = system.accounts.get_SR_cost_per_trade_for_instrument(instrument_code)

    trading_cost = turnover * SR_cost_per_trade

    return trading_cost


def net_SR_for_instrument(maximum_position, trading_cost, notional_SR=0.5):
    return notional_SR - trading_cost - size_penalty(maximum_position)


def size_penalty(maximum_position):
    if maximum_position < 0.5:
        return 9999
    return 0.125 / maximum_position ** 2


def get_system():
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
    my_config.instruments = get_etf_instruments()

    my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3, ewmac16=3.75)
    my_config.use_forecast_scale_estimates = False

    fcs = ForecastScaleCap()

    # estimates:
    my_account = Account()
    combiner = ForecastCombine()
    raw_data = RawData()

    # 使用固定预测权重
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
    my_config.use_instrument_weight_estimates = True
    my_config.use_instrument_div_mult_estimates = True
    my_config.instrument_weight_estimate = dict(
        method="shrinkage", date_method="expanding")

    my_config.forecast_floor = 0
    my_system = System(
        [fcs, my_rules, combiner, possizer, portfolio, my_account, raw_data], data, my_config
    )
    return my_system


def portfolio_sizes_and_SR_for_instrument_list(system, corr_matrix, instrument_list):

    estimates = build_estimates(
        instrument_list=instrument_list,
        corr_matrix=corr_matrix)

    handcraft_portfolio = handcraftPortfolio(estimates)
    risk_weights = handcraft_portfolio.risk_weights()

    SR = estimate_SR_given_weights(system=system,
                                   risk_weights=risk_weights,
                                   handcraft_portfolio=handcraft_portfolio)

    portfolio_sizes = estimate_portfolio_sizes_given_weights(system,
                                                             risk_weights=risk_weights,
                                                             handcraft_portfolio=handcraft_portfolio)

    return portfolio_sizes, SR


def build_estimates(instrument_list, corr_matrix, notional_years_data=30):
    # we ignore differences in SR for creating instrument weights

    mean_estimates = meanEstimates(dict([
        (instrument_code, 1.0)
        for instrument_code in instrument_list
    ]))

    stdev_estimates = stdevEstimates(dict([
        (instrument_code, 1.0) for instrument_code in instrument_list
    ]))

    estimates = Estimates(correlation=corr_matrix.subset(instrument_list),
                          mean=mean_estimates,
                          stdev=stdev_estimates,
                          frequency="W",
                          data_length=notional_years_data * WEEKS_IN_YEAR)

    return estimates


def estimate_SR_given_weights(system, risk_weights, handcraft_portfolio: handcraftPortfolio):
    instrument_list = list(risk_weights.keys())

    mean_estimates = mean_estimates_from_SR_function_actual_weights(system,
                                                                    risk_weights=risk_weights,
                                                                    handcraft_portfolio=handcraft_portfolio)
    print(mean_estimates)
    print(instrument_list)
    wt = np.array(risk_weights.as_list_given_keys(instrument_list))
    mu = np.array(mean_estimates.list_in_key_order(instrument_list))
    cm = handcraft_portfolio.estimates.correlation_matrix

    SR = -neg_SR(wt, cm, mu)

    return SR


def mean_estimates_from_SR_function_actual_weights(system, risk_weights, handcraft_portfolio: handcraftPortfolio):
    instrument_list = list(risk_weights.keys())
    actual_idm = min(2.5, handcraft_portfolio.div_mult(risk_weights))
    mean_estimates = meanEstimates(dict([
        (instrument_code, net_SR_for_instrument_in_system(system, instrument_code,
                                                          instrument_weight_idm=actual_idm * risk_weights[
                                                              instrument_code]))
        for instrument_code in instrument_list
    ]))

    return mean_estimates


def estimate_portfolio_sizes_given_weights(system, risk_weights, handcraft_portfolio: handcraftPortfolio):
    instrument_list = list(risk_weights.keys())
    idm = handcraft_portfolio.div_mult(risk_weights)

    portfolio_sizes = dict([
        (instrument_code,
         round(calculate_maximum_position(system,
                                          instrument_code,
                                          instrument_weight_idm=risk_weights[instrument_code] * idm), 1))

        for instrument_code in instrument_list
    ])

    return portfolio_sizes


if __name__ == '__main__':
    max_instrument_weight = 0.05
    notional_starting_IDM = 1
    minimum_instrument_weight_idm = max_instrument_weight * notional_starting_IDM

    system = get_system()
    list_of_instruments = system.get_instrument_list()
    print(list_of_instruments)
    all_results = []
    for instrument_code in list_of_instruments:
        all_results.append((instrument_code,
                            net_SR_for_instrument_in_system(system, instrument_code)))

    all_results = sorted(all_results, key=lambda tup: tup[1])

    print(all_results)
    best_market = all_results[-1][0]

    list_of_correlations = system.portfolio.get_instrument_correlation_matrix()
    corr_matrix = list_of_correlations.corr_list[-1]

    set_of_instruments_used = [best_market]

    unused_list_of_instruments = copy(list_of_instruments)
    unused_list_of_instruments.remove(best_market)
    max_SR = 0.0
    while len(unused_list_of_instruments) > 0:
        SR_list = []
        portfolio_sizes_dict = {}
        for instrument_code in unused_list_of_instruments:
            instrument_list = set_of_instruments_used + [instrument_code]
            print(instrument_list)
            portfolio_sizes, SR_this_instrument = \
                portfolio_sizes_and_SR_for_instrument_list(system,
                                                           corr_matrix=corr_matrix,
                                                           instrument_list=instrument_list)
            SR_list.append((instrument_code, SR_this_instrument))
            portfolio_sizes_dict[instrument_code] = portfolio_sizes

        SR_list = sorted(SR_list, key=lambda tup: tup[1])
        selected_market = SR_list[-1][0]
        new_SR = SR_list[-1][1]
        if (new_SR) < (max_SR * .9):
            print("PORTFOLIO TOO BIG! SR falling")
            break
        portfolio_size_with_market = portfolio_sizes_dict[selected_market]
        print("Portfolio %s SR %.2f" % (str(set_of_instruments_used), new_SR))
        print(str(portfolio_size_with_market))

        set_of_instruments_used.append(selected_market)
        unused_list_of_instruments.remove(selected_market)
        if new_SR > max_SR:
            max_SR = new_SR