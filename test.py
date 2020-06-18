import numpy as np
from talib import abstract
import matplotlib.pyplot as plt
from Views import PyPlotPlotter
from Scrapers import NordnetOOPScraper

SMA = abstract.Function('SMA')
WMA = abstract.Function('WMA')
EMA = abstract.Function('EMA')
ADX = abstract.Function('ADX')
ROC = abstract.Function('ROC')
LINREG = abstract.Function('LINEARREG_SLOPE')
series = next(iter((NordnetOOPScraper.main()).values()))

#print(np.asarray(series['OPEN']))

ADX_data = ADX(np.asarray(series['OPEN']), np.asarray(series['HIGH']), np.asarray(series['LOW']), timeperiod=14)
SMA_data = SMA(np.asarray(series['CLOSE']), timeperiod=7)
WMA_data = WMA(np.asarray(series['CLOSE']), timeperiod=7)
EMA_data = EMA(np.asarray(series['CLOSE']), timeperiod=7)
ROC_data = ROC(np.asarray(series['CLOSE']))
ADX_SMA_data = SMA(ADX_data, timeperiod=21)
ADX_EMA_data = EMA(ADX_data, timeperiod=21)

reg_data = LINREG(np.asarray(series['CLOSE']))


"""SMA_OPEN, SMA_HIGH, SMA_LOW = SMA(np.asarray(series['OPEN']), timeperiod=7),\
                                SMA(np.asarray(series['HIGH']), timeperiod=7),\
                                SMA(np.asarray(series['LOW']), timeperiod=7)
ADX_SMA_data = ADX(SMA_OPEN, SMA_HIGH, SMA_LOW)"""

"""PyPlotPlotter.plot_two_graphs_two_scales(np.asarray(series['TIME']), np.asarray(series['CLOSE']),
                                         np.asarray(series['TIME']), ADX_SMA_data,
                                         LABEL_1="High data", LABEL_2="ADX",
                                         Y_LABEL_1="NOK", Y_LABEL_2="Momentum")"""

PyPlotPlotter.plot_two_graphs_two_scales(np.asarray(series['TIME']), np.asarray(series['CLOSE']),
                                         np.asarray(series['TIME']), ROC_data,
                                         LABEL_1="High data", LABEL_2="ROC",
                                         Y_LABEL_1="NOK", Y_LABEL_2="Momentum")

"""PyPlotPlotter.plot_three_graphs_one_scale(np.asarray(series['TIME']), SMA_data, EMA_data, series['CLOSE'],
                                        X_LABEL="Time", Y_LABEL="mom",
                                        LABEL_1="ADX SMA", LABEL_2="ADX WMA", LABEL_3='series')"""

"""PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), reg_data,
                                        X_LABEL="Time", Y_LABEL="Nok",
                                        LABEL_1="CLOSE", LABEL_2="REG")"""

# TODO: ADX TA on SMA filtered OHL data set
