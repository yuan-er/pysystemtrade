"""
This is a variation of the chapter 15 system which estimates rather than uses
fixed parameters

A system consists of a system, plus a config

"""
from syscore.objects import arg_not_supplied
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.config.configdata import Config

from systems.forecasting import Rules
from systems.basesystem import System
from systems.forecast_combine import ForecastCombine
from systems.forecast_scale_cap import ForecastScaleCap
from systems.futures.rawdata import FuturesRawData
from systems.positionsizing import PositionSizing
from systems.portfolio import Portfolios
from systems.accounts.accounts_stage import Account


def futures_system(
        data=None,
        config=None,
        trading_rules=arg_not_supplied,
        log_level="on"):
    """

    :param data: data object (defaults to reading from csv files)
    :type data: sysdata.data.simData, or anything that inherits from it

    :param config: Configuration object (defaults to futuresconfig.yaml in this directory)
    :type config: sysdata.configdata.Config

    :param trading_rules: Set of trading rules to use (defaults to set specified in config object)
    :param trading_rules: list or dict of TradingRules, or something that can be parsed to that

    :param log_level: Set of trading rules to use (defaults to set specified in config object)
    :type log_level: str

    """

    if data is None:
        data = csvFuturesSimData()

    if config is None:
        config = Config(
            "systems.provided.ewmac_carry.futuresestimateconfig.yaml")

    rules = Rules(trading_rules)

    system = System(
        [
            Account(),
            Portfolios(),
            PositionSizing(),
            FuturesRawData(),
            ForecastCombine(),
            ForecastScaleCap(),
            rules,
        ],
        data,
        config,
    )

    system.set_logging_level(log_level)

    return system


if __name__ == "__main__":
    import doctest

    doctest.testmod()
