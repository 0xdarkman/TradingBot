from Views import PyPlotPlotter, PlotlyPlotter
from Scrapers import NordnetScraper
from Controllers.TAlibWrapper import *
from Models import TIModel

series = next(iter((NordnetScraper.main(GET_SERIES='SINGLE', TICKER='ENDUR', PERIOD='6d', TIME_TYPE='DATETIME')).values()))
time_series = series['TIME']
open_series = series['OPEN']
high_series = series['HIGH']
low_series = series['LOW']
close_series = series['CLOSE']
volume_series = series['VOLUME']


BBANDS_data = BBANDS(close_series, SMOOTH=True)

ADX_data = ADX(high_series, low_series, close_series, PERIOD=21)
SLOPE_data = SLOPE_REG(close_series, SMOOTH=True)

MOM_data = MOM(close_series)
"""ROC2_data = ROC(BBANDS_data[2], 2)
ROC2_data = SMA(ROC2_data, 2)"""

WMA_data = WMA(close_series)
SMA_data = SMA(close_series)
EMA_data = EMA(close_series)
MACD_data = MACD(close_series)

BBANDS_DIFF_data = TIModel.BBANDS_close_diff(close_series, ROC=True)
MACD_DIFF_data = TIModel.MACD_signal_diff(close_series, DIFF_PCT=True)

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_DIFFcloseNupBB=dict(PLOT=BBANDS_DIFF_data[0], COLOR='darkviolet', DASH='solid', Y_AXIS='Diff', MODE='none'),
                             GRAPH_2_DIFFcloseNloBB=dict(PLOT=BBANDS_DIFF_data[1], COLOR='green', DASH='solid', Y_AXIS='Diff', MODE='none'))"""


PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_DIFFmacdNsignal=dict(PLOT=MACD_DIFF_data, COLOR='darkgreen', DASH='solid', Y_AXIS='DiffMACD', MODE='none'))

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'))"""

"""PyPlotPlotter.plot_graphs_one_scale(time_series, X_LABEL="Time", Y_LABEL="NOK",
                                    MACD_0=MACD_data[0], MACD_1=MACD_data[1], MACD_2=MACD_data[2])

PyPlotPlotter.plot_graphs_two_scales(time_series, Y_LABEL_1="NOK", Y_LABEL_2="ADX", COLORS_DIFF=True,
                                     GRAPH_1_CLOSE=close_series,
                                     GRAPH_2_MACD=MACD_data[0], GRAPH_2_MACD_signal_line=MACD_data[1])"""
