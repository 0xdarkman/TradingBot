from Views import PyPlotPlotter, PlotlyPlotter
from Scrapers import NordnetScraper
from Controllers.TAlibWrapper import *
from Models import TIModels

series = next(iter((NordnetScraper.main(GET_SERIES='SINGLE', TICKER='NEL', PERIOD='1d', TIME_TYPE='DATETIME')).values()))
time_series = series['TIME']
open_series = series['OPEN']
high_series = series['HIGH']
low_series = series['LOW']
close_series = series['CLOSE']
volume_series = series['VOLUME']

hours = 8
TIME_cut = SERIES_CUTOFF(time_series, close_series, N_HOURS=hours)[0]
CLOSE_cut = SERIES_CUTOFF(time_series, close_series, N_HOURS=hours)[1]
HIGH_cut = SERIES_CUTOFF(time_series, high_series, N_HOURS=hours)[1]
LOW_cut = SERIES_CUTOFF(time_series, low_series, N_HOURS=hours)[1]


BBANDS_data = BBANDS(CLOSE_cut, NBDEVUP=3.9, NBDEVDN=3.9)

ADX_data = ADX(HIGH_cut, LOW_cut, CLOSE_cut, PERIOD=21)
SLOPE_data = SLOPE_REG(close_series, SMOOTH=True)

MOM_data = MOM(close_series)
"""ROC2_data = ROC(BBANDS_data[2], 2)
ROC2_data = SMA(ROC2_data, 2)"""

WMA_data = WMA(close_series)
SMA_data = SMA(close_series)
EMA_data = EMA(close_series)
MACD_data = MACD(close_series)

RSI_data = RSI(CLOSE_cut)

rsi_trigg = TIModels.RSI_trigger(CLOSE_cut, DEBUG=True)

macd_diff = TIModels.MACD_signal_diff(CLOSE_cut, NORMALIZED=True)
macd_trigg = TIModels.MACD_signal_normalized_trigger(CLOSE_cut, DEBUG=True)

bbands_trigg = TIModels.BBANDS_trigger(CLOSE_cut, DEBUG=True)

bbands_trigg_roc = TIModels.BBANDS_ROC_trigger(CLOSE_cut, DEBUG=True)

PlotlyPlotter.plot_line_sets(TIME_cut,
                             GRAPH_1_CLOSE=dict(PLOT=CLOSE_cut, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_RSI=dict(PLOT=RSI_data, COLOR='darkviolet', DASH='solid', Y_AXIS='RSI', MODE='none'))

"""
PlotlyPlotter.plot_line_sets(TIME_cut,
                             GRAPH_1_bbupper_diff_roc=dict(PLOT=BBANDS_DIFF_data[0], COLOR='red', DASH='none', Y_AXIS='ROC'),
                             GRAPH_1_bblower_diff_roc=dict(PLOT=BBANDS_DIFF_data[1], COLOR='blue', DASH='none', Y_AXIS='ROC'),
                             GRAPH_2_MACD=dict(PLOT=MACD_DIFF_data, COLOR='darkgreen', DASH='solid', Y_AXIS='MACD', MODE='none'))


PlotlyPlotter.plot_line_sets(TIME_cut,
                             GRAPH_1_CLOSE=dict(PLOT=CLOSE_cut, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_ADX=dict(PLOT=ADX_data, COLOR='darkviolet', DASH='solid', Y_AXIS='ADX', MODE='none'))
"""

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_DIFFmacdNsignal=dict(PLOT=MACD_DIFF_NORMAL_data, COLOR='darkgreen', DASH='solid', Y_AXIS='DiffMACD', MODE='none'))
"""

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'))"""

"""PyPlotPlotter.plot_graphs_one_scale(time_series, X_LABEL="Time", Y_LABEL="NOK",
                                    MACD_0=MACD_data[0], MACD_1=MACD_data[1], MACD_2=MACD_data[2])

PyPlotPlotter.plot_graphs_two_scales(time_series, Y_LABEL_1="NOK", Y_LABEL_2="ADX", COLORS_DIFF=True,
                                     GRAPH_1_CLOSE=close_series,
                                     GRAPH_2_MACD=MACD_data[0], GRAPH_2_MACD_signal_line=MACD_data[1])"""
