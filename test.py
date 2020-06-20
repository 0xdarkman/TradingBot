from Views import PyPlotPlotter
from Scrapers import NordnetScraper
from Controllers.TAlibWrapper import *

series = next(iter((NordnetScraper.main(GET_SERIES='SINGLE', TICKER='ENDUR', PERIOD='6d')).values()))
time_series = series['TIME']
open_series = series['OPEN']
high_series = series['HIGH']
low_series = series['LOW']
close_series = series['CLOSE']
volume_series = series['VOLUME']

BBANDS_data = BBANDS(close_series, SMOOTH=True)

ADX_data = ADX(high_series, low_series, close_series, PERIOD=30)

SLOPE_data = SLOPE_REG(close_series, SMOOTH=True)

MOM_data = MOM(close_series)
ROC_data = ROC(close_series)

WMA_data = WMA(close_series)
SMA_data = SMA(close_series)
EMA_data = EMA(close_series)

MACD_data = MACD(close_series)


PyPlotPlotter.plot_graphs_one_scale(time_series, X_LABEL="Time", Y_LABEL="NOK",
                                    MACD_0=MACD_data[0], MACD_1=MACD_data[1], MACD_2=MACD_data[2])

PyPlotPlotter.plot_graphs_two_scales(time_series, Y_LABEL_1="NOK", Y_LABEL_2="ADX", COLORS_DIFF=True,
                                     GRAPH_1_CLOSE=close_series,
                                     GRAPH_2_MACD=MACD_data[0], GRAPH_2_MACD_signal_line=MACD_data[1])
