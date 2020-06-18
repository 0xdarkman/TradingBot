from Views import PyPlotPlotter
from Scrapers import NordnetScraper
from Controllers import TAlibWrapper

series = next(iter((NordnetScraper.main()).values()))

time_series = series['TIME']
open_series = series['OPEN']
high_series = series['HIGH']
low_series = series['LOW']
close_series = series['CLOSE']
volume_series = series['VOLUME']

WMA_data = TAlibWrapper.WMA(close_series)
BBANDS_data = TAlibWrapper.BBANDS(close_series, SMOOTH=True)
print(BBANDS_data)

# TODO: BBANDS combined with ADX or MOM

"""PyPlotPlotter.plot_two_graphs_two_scales(time_series, WMA_data,
                                         time_series, SLOPE_data,
                                         LABEL_1="CLOSE data", LABEL_2="ROC",
                                         Y_LABEL_1="NOK", Y_LABEL_2="rate of change")"""

PyPlotPlotter.plot_three_graphs_one_scale(time_series, BBANDS_data[0], close_series, BBANDS_data[2],
                                          X_LABEL="Time", Y_LABEL="Nok",
                                          LABEL_1="bbands upper", LABEL_2="CLOSE series", LABEL_3='bbands lower')

"""PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), reg_data,
                                        X_LABEL="Time", Y_LABEL="Nok",
                                        LABEL_1="CLOSE", LABEL_2="REG")"""
