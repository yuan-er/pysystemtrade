import pandas as pd
from systems.provided.ewmac_carry.estimatedsystem import futures_system

my_system = futures_system(log_level="on")

print(my_system.accounts.portfolio().sharpe())

profits = my_system.accounts.portfolio()
print(profits.percent.stats())
print(my_system.accounts.get_notional_capital())
profits.curve().plot()
from matplotlib.pyplot import show

show()
# print(my_system.rawdata.get_instrument_raw_carry_data("161912").tail(5))
# from systems.provided.ewmac_carry.rules import carry2
# print(carry2(my_system.rawdata.get_instrument_raw_carry_data("161912")).tail(5))

print(my_system.combForecast.get_combined_forecast("161912").tail(5))

print(profits.gross.percent.stats())
print(profits.net.percent.stats())

# instruments_weight_df = my_system.portfolio.get_instrument_weights()
# idm_df = my_system.portfolio.get_instrument_diversification_multiplier()
# # print(idm_df)
# # print(my_system.combForecast.get_combined_forecast())
# # print(my_system.positionSize.get_volatility_scalar())
# forecast_combine_df = pd.DataFrame()
# volatility_combine_df = pd.DataFrame()
#
# for code in my_config.instruments:
#     code_forecast = my_system.combForecast.get_combined_forecast(code)
#     volatility_scalar = my_system.positionSize.get_volatility_scalar(code)
#     forecast_combine_df = forecast_combine_df.append(code_forecast, ignore_index=True)
#     volatility_combine_df = volatility_combine_df.append(volatility_scalar, ignore_index=True)
#     # print(code)
#     # print(my_system.accounts.get_actual_position(code).tail(5))
#
# # print(my_system.forecastScaleCap.get_capped_forecast("159949", "ewmac4").tail(5))
# # print(my_system.rawdata.daily_returns_volatility("159949").tail(5))
# # print(my_system.forecastScaleCap.get_raw_forecast("159949", "ewmac4").tail(5))
# forecast_combine_df = forecast_combine_df.T
# forecast_combine_df.columns = my_config.instruments
# volatility_combine_df = volatility_combine_df.T
# volatility_combine_df.columns = my_config.instruments
# instruments_weight_df.to_csv('weight.csv')
# idm_df.to_csv('idm.csv')
# forecast_combine_df.to_csv('forecast.csv')
# volatility_combine_df.to_csv('vol.csv')
# print(my_system.portfolio.get_instrument_weights().tail(1).to_dict(orient='records'))