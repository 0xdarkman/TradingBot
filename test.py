import numpy as np
from talib import abstract
import matplotlib.pyplot as plt
from Views import PyPlotPlotter
from Scrapers import NordnetOOPScraper

x = [x for x in range(100)]
close = np.sin(x)
SMA = abstract.Function('SMA')
ADX = abstract.Function('ADX')

series = next(iter((NordnetOOPScraper.main()).values()))

#print(np.asarray(series['OPEN']))

ADX_data = ADX(np.asarray(series['OPEN']), np.asarray(series['HIGH']), np.asarray(series['LOW']))
SMA_data = SMA(np.asarray(series['CLOSE']), timeperiod=21)

PyPlotPlotter.plot_two_graphs_two_scales(np.asarray(series['TIME']), np.asarray(series['HIGH']),
                                         [x for x in range(len(ADX_data))], ADX_data,
                                         LABEL_1="High data", LABEL_2="ADX",
                                         Y_LABEL_1="NOK", Y_LABEL_2="Momentum")

PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), SMA_data,
                                        X_LABEL="Time", Y_LABEL="NOK",
                                        LABEL_1="Close data", LABEL_2="SMA21")

# TODO: ADX TA on SMA filtered OHL data set
