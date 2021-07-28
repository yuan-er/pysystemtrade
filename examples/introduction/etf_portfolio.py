# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2021-07-27"

"""
验证etf组合是否与backtrader计算结果一致
"""
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
# my_rules = Rules(dict(ewmac8=ewmac_8, ewmac16=ewmac_16))

my_config = Config()
empty_rules = Rules()
my_config.trading_rules = dict(ewmac4=ewmac_4, ewmac8=ewmac_8, ewmac16=ewmac_16)
# my_config.trading_rules = dict(ewmac8=ewmac_8, ewmac16=ewmac_16)

# we can estimate these ourselves
my_config.instruments = ['159949', '510050', '510330', '501077', '161912', '501046',
                         '163417', '161005', '513050', '513100', '160416']
my_config.use_forecast_scale_estimates = True
my_config.start_date = '2020-01-01'

# my_config.forecast_scalars = dict(ewmac4=7.5, ewmac8=5.3, ewmac16=3.75)
# my_config.use_forecast_scale_estimates = False

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
    method="shrinkage", date_method="in_sample")


# or fixed
# portfolio = Portfolios()
# my_config.use_instrument_weight_estimates = False
# my_config.use_instrument_div_mult_estimates = False
# my_config.instrument_weights = dict(US10=0.1, EDOLLAR=0.4, CORN=0.3, SP500=0.2)
# my_config.instrument_div_multiplier = 1.5
#
# my_system = System([fcs, my_rules, combiner, possizer,
#                     portfolio, raw_data], data, my_config)
#
"""
Have we made some dosh?
"""
print(my_config.start_date)
exit()
my_system = System(
    [fcs, my_rules, combiner, possizer, portfolio, my_account, raw_data], data, my_config
)
my_system.set_logging_level("on")


profits = my_system.accounts.portfolio()
# print(profits.percent.stats())
profits.curve().plot()
from matplotlib.pyplot import show
show()

# have costs data now
print(profits.gross.percent.stats())
print(profits.net.percent.stats())

print(my_system.positionSize.get_price_volatility("159949").tail(5))
print(my_system.positionSize.get_block_value("159949").tail(5))
print(my_system.positionSize.get_underlying_price("159949"))
print(my_system.positionSize.get_instrument_value_vol("159949").tail(5))
print(my_system.positionSize.get_volatility_scalar("159949").tail(5))
print(my_system.positionSize.get_vol_target_dict())
print(my_system.positionSize.get_subsystem_position("159949").tail(5))

print(my_system.portfolio.get_instrument_weights().tail(5))
print(my_system.portfolio.get_instrument_diversification_multiplier().tail(5))
for code in my_config.instruments:
    print(code)
    print(my_system.positionSize.get_subsystem_position(code).tail(5)) # 子系统仓位
    print(my_system.portfolio.get_notional_position(code).tail(5)) # 最终系统仓位
