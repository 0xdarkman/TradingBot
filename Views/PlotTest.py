from Views import PyPlotPlotter, PlotlyPlotter
from Scrapers import NordnetScraper
from Controllers.TAlibWrapper import *

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
ROC2_data = ROC(close_series, 2)
ROC7_data = ROC(close_series, 7)

WMA_data = WMA(close_series)
SMA_data = SMA(close_series)
EMA_data = EMA(close_series)
MACD_data = MACD(close_series)

DIFFcloseNupBB_data = DIFF(close_series, BBANDS_data[0])[0]
DIFFcloseNloBB_data = DIFF(BBANDS_data[2], close_series)[0]
DIFFmacdNsignal_data = DIFF(MACD_data[0], MACD_data[1])

for i in range(len(DIFFcloseNupBB_data)):
    if DIFFcloseNupBB_data[i] < 0.0:
        DIFFcloseNupBB_data[i] = None
    if DIFFcloseNloBB_data[i] < 0.0:
        DIFFcloseNloBB_data[i] = None

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'))"""

"""PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_MACD=dict(PLOT=MACD_data[0], COLOR='violet', DASH='dashdot', Y_AXIS='MACD'),
                             GRAPH_2_Signal_line=dict(PLOT=MACD_data[1], COLOR='green', DASH='solid', Y_AXIS='MACD'))"""
PlotlyPlotter.plot_line_sets(time_series,
                             GRAPH_1_CLOSE=dict(PLOT=close_series, COLOR='red', DASH='solid', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_upper=dict(PLOT=BBANDS_data[0], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_1_BBAND_lower=dict(PLOT=BBANDS_data[2], COLOR='blue', DASH='dash', Y_AXIS='NOK'),
                             GRAPH_2_DIFFcloseNupBB=dict(PLOT=DIFFcloseNupBB_data, COLOR='darkviolet', DASH='solid', Y_AXIS='Diff', MODE='markers'),
                             GRAPH_2_DIFFcloseNloBB=dict(PLOT=DIFFcloseNloBB_data, COLOR='green', DASH='solid', Y_AXIS='Diff', MODE='markers'),
                             GRAPH_2_DIFFmacdNsignal=dict(PLOT=DIFFmacdNsignal_data[0], COLOR='gold', DASH='solid', Y_AXIS='Diff', MODE='none'))


"""PyPlotPlotter.plot_graphs_one_scale(time_series, X_LABEL="Time", Y_LABEL="NOK",
                                    MACD_0=MACD_data[0], MACD_1=MACD_data[1], MACD_2=MACD_data[2])

PyPlotPlotter.plot_graphs_two_scales(time_series, Y_LABEL_1="NOK", Y_LABEL_2="ADX", COLORS_DIFF=True,
                                     GRAPH_1_CLOSE=close_series,
                                     GRAPH_2_MACD=MACD_data[0], GRAPH_2_MACD_signal_line=MACD_data[1])"""
