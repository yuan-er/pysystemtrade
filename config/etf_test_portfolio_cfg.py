# coding: utf-8
# -*- coding:utf-8 -*-
__author__ = "qiang"
__license__ = ""
__version__ = "2021-07-06"

"""
预定义用于投资的场内ETF
"""

etf_instruments = dict()
etf_names = dict()

# 指数ETF 10w
etf_instruments['159949.sz'] = '2016-06-30'  # 创业板50 可融资可卖空
etf_names['159949.sz'] = '创业板50'

etf_instruments['510050.sh'] = '2004-12-30'  # 上证50ETF 可融资可卖空
etf_names['510050.sh'] = '上证50'

etf_instruments['510330.sh'] = '2012-12-25'  # 300ETF基金 可融资可卖空
etf_names['510330.sh'] = '300ETF'

etf_instruments['510500.sh'] = '2013-02-06'  # 中证500ETF 可融资可卖空
etf_names['510500.sh'] = '500ETF'

etf_instruments['588000.sh'] = '2020-09-28' # 科创50ETF 可融资可卖空
etf_names['588000.sh'] = '科创50'

# 封闭基金 8w
etf_instruments['501077.sh'] = '2019-06-11'  # 科创富国 到期2022-06-11
etf_names['501077.sh'] = '科创富国'

etf_instruments['161912.sz'] = '2019-06-11'  # 社会责任 到期2022-04-17
etf_names['161912.sz'] = '社会责任'

etf_instruments['501046.sh'] = '2017-10-23'  # 财通福鑫 到期2022-04-27
etf_names['501046.sh'] = '财通福鑫'

etf_instruments['162720.sz'] = '2020-09-24'  # 创业广发
etf_instruments['160529.sz'] = '2020-09-03'  # 创业博时
etf_instruments['506002.sh'] = '2020-07-28'  # 易方达科创板
etf_instruments['506005.sh'] = '2020-07-29'  # 科创板博时
etf_instruments['501093.sh'] = '2020-03-06'  # 华夏翔阳LOF


# 开放基金 4w
etf_instruments['163417.sz'] = '2018-01-23'  # 兴全合宜
etf_names['163417.sz'] = '兴全合宜'

etf_instruments['161005.sz'] = '2005-11-16'  # 富国天惠
etf_names['161005.sz'] = '富国天惠'

# 行业 2w
etf_instruments['513050.sh'] = '2017-01-04'  # 中概互联网ETF
etf_names['513050.sh'] = '中概互联'

etf_instruments['512800.sh'] = '2017-07-18'  # 银行ETF
etf_instruments['159928.sz'] = '2013-08-23'  # 消费ETF
etf_instruments['159929.sz'] = '2013-08-23'  # 医药ETF
etf_instruments['512000.sh'] = '2016-08-30'  # 券商ETF
etf_instruments['512200.sh'] = '2017-08-25'  # 房地产ETF
etf_instruments['512580.sh'] = '2017-01-25'  # 环保ETF
etf_instruments['512660.sh'] = '2016-07-26'  # 军工ETF
etf_instruments['161631.sz'] = '2017-04-10'  # 人工智能ETF

# 国外指数 4w
etf_instruments['513100.sh'] = '2013-04-25'  # 纳指ETF
etf_names['513100.sh'] = '纳指ETF'

etf_instruments['513500.sh'] = '2013-12-05'  # 标普500ETF
etf_names['513500.sh'] = '标普500ETF'

etf_instruments['513080.sh'] = '2020-05-29'  # 法国CAC40ETF
etf_instruments['513030.sh'] = '2014-08-08'  # 德国30ETF
etf_instruments['513520.sh'] = '2019-06-12'  # 日经ETF
etf_instruments['510900.sh'] = '2012-08-09'  # H股ETF


# 黄金ETF 2w
etf_instruments['518880.sh'] = '2013-07-18'  # 黄金ETF
etf_names['518880.sh'] = '黄金ETF'

# 原油ETF
etf_instruments['160416.sz'] = '2012-03-29'  # 原油ETF
etf_names['160416.sz'] = '原油ETF'

etf_instruments['162411.sz'] = '2011-09-29'  # 华宝油气
etf_instruments['160723.sz'] = '2017-04-20'  # 嘉实原油
etf_instruments['501018.sh'] = '2016-06-15'  # 南方原油LOF



# bootstrap
# etf_instruments_weight = [0.009965, 0.043564, 0.005055, 0.107490, 0.188505,
#                           0.072961, 0.089543, 0.078148, 0.044626, 0.180371,
#                           0.109091, 0.070682] # v0 去除黄金
# etf_instruments_weight = [0.11542, 0.239408, 0.062245, 0.208868, 0.091709,
#                           0.061549, 0.100571, 0.076372, 0.043857]  # 去除黄金和指数基金
etf_instruments_weight = [0.007071, 0.031397, 0.009435, 0.086602, 0.144870,
                          0.063739, 0.063142, 0.065914, 0.045625, 0.145418,
                          0.100096, 0.188981, 0.047710] # 全部包含

# etf_instruments_weight = [0.067071, 0.031397, 0.029435, 0.116602, 0.144870,
#                           0.123739, 0.063142, 0.065914, 0.065625, 0.075418,
#                           0.060096, 0.068981, 0.087710] # 手动调整


# etf_instruments_weight = [0.077914, 0.080912, 0.116048, 0.090865, 0.066841,
#                           0.161088, 0.062166, 0.121851, 0.122540, 0.099776]  # 去除黄金和指数基金 + A50

# etf_instruments_weight = [0.009116, 0.038377, 0.006386, 0.004004, 0.126663,
#                           0.197947, 0.085886, 0.084446, 0.072076, 0.050932,
#                           0.156453, 0.097586, 0.070128]  # 去除黄金 + etf500
# etf_instruments_weight = [0.006219, 0.010628, 0.000972, 0.113918, 0.149871,
#                           0.052265, 0.054555, 0.036658, 0.034433, 0.034428,
#                           0.094777, 0.031647, 0.007528, 0.008739, 0.014551,
#                           0.011736, 0.012387, 0.138692, 0.125196, 0.060799] # 去除黄金，加入更多行业etf

# origin_data = tc.get_etf_histtory_daily_data('159883.sz', '2016-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '159883.sz' + "_data.csv", index=False)
# instruments.append('159883.sz')

# origin_data = tc.get_etf_histtory_daily_data('161721.sz', '2016-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '161721.sz' + "_data.csv", index=False)
# instruments.append('161721.sz')

# origin_data = tc.get_etf_histtory_daily_data('161030.sz', '2016-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '161030.sz' + "_data.csv", index=False)
# instruments.append('161030.sz')

# origin_data = tc.get_etf_histtory_daily_data('159825.sz', '2016-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '159825.sz' + "_data.csv", index=False)
# instruments.append('159825.sz')

# origin_data = tc.get_etf_histtory_daily_data('159913.sz', '2016-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '159913.sz' + "_data.csv", index=False)
# instruments.append('159913.sz')

# origin_data = tc.get_etf_histtory_daily_data('163417.sz', '2018-12-28')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '163417.sz' + "_data.csv", index=False)

# origin_data = tc.get_etf_histtory_daily_data('159861.sz', '2020-1-1')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '159861.sz' + "_data.csv", index=False)
# instruments.append('159861.sz')

# origin_data = tc.get_etf_histtory_daily_data('510660.sh', '2013-1-1')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '510660.sh' + "_data.csv", index=False)
# instruments.append('510660.sh')

# origin_data = tc.get_etf_histtory_daily_data('159863.sz', '2020-1-1')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '159863.sz' + "_data.csv", index=False)
# instruments.append('159863.sz')

# origin_data = tc.get_etf_histtory_daily_data('516070.sh', '2020-1-1')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '516070.sh' + "_data.csv", index=False)
# instruments.append('516070.sh')

# origin_data = tc.get_etf_histtory_daily_data('512480.sh', '2018-1-1')
# new_df = convert_tushare_2_backtrader(origin_data)
# new_df.to_csv(etf_working_path + "history_" + '512480.sh' + "_data.csv", index=False)
# instruments.append('512480.sh')
