import numpy as np
from talib import abstract
from Views import PyPlotPlotter
from Scrapers import NordnetOOPScraper

# Functions used in this wrapper.
# Set them in front so that they load on import.
SMA_func = abstract.Function('SMA')
WMA_func = abstract.Function('WMA')
ADX_func = abstract.Function('ADX')
SLOPE_REG_func = abstract.Function('LINEARREG_SLOPE')


def SMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of simple moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return SMA_func(np_array, timeperiod=PERIOD)


def WMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of weighted moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return WMA_func(np_array, timeperiod=PERIOD)


def ADX(DATA_LIST_OPEN, DATA_LIST_HIGH, DATA_LIST_LOW, PERIOD=21, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	:param DATA_LIST_OPEN: list/array of numbers: period open values
	:param DATA_LIST_HIGH: list/array of numbers: period high values
	:param DATA_LIST_LOW: list/array of numbers: period low values
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return: array of ADX values
	"""
	np_array_open = np.asarray(DATA_LIST_OPEN)
	np_array_high = np.asarray(DATA_LIST_HIGH)
	np_array_low = np.asarray(DATA_LIST_LOW)

	ADX_data = ADX_func(np_array_open, np_array_high, np_array_low, timeperiod=PERIOD)
	if not SMOOTH:
		return ADX_data
	else:
		return SMA(ADX_data, PERIOD=SMOOTH_PERIOD)


def SLOPE_REG(DATA_LIST, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	:param DATA_LIST:
	:param SMOOTH:
	:param SMOOTH_PERIOD:
	:return:
	"""
	np_array = np.asarray(DATA_LIST)

	SLOPE_REG_data = SLOPE_REG_func(np_array)
	if not SMOOTH:
		return SLOPE_REG_data
	else:
		return SMA(SLOPE_REG_data, PERIOD=SMOOTH_PERIOD)


series = next(iter((NordnetOOPScraper.main()).values()))


ADX_SMA_data = SMA(ADX_data, timeperiod=5)

reg_data = LINREG(np.asarray(series['CLOSE']))


"""SMA_OPEN, SMA_HIGH, SMA_LOW = SMA(np.asarray(series['OPEN']), timeperiod=7),\
                                SMA(np.asarray(series['HIGH']), timeperiod=7),\
                                SMA(np.asarray(series['LOW']), timeperiod=7)
ADX_SMA_data = ADX(SMA_OPEN, SMA_HIGH, SMA_LOW)"""

PyPlotPlotter.plot_two_graphs_two_scales(np.asarray(series['TIME']), np.asarray(series['CLOSE']),
                                         np.asarray(series['TIME']), reg_data,
                                         LABEL_1="High data", LABEL_2="ADX",
                                         Y_LABEL_1="NOK", Y_LABEL_2="Momentum", ROTATE=True)

"""PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), SMA_data,
                                        X_LABEL="Time", Y_LABEL="NOK",
                                        LABEL_1="Close data", LABEL_2="SMA21")"""

"""PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), reg_data,
                                        X_LABEL="Time", Y_LABEL="Nok",
                                        LABEL_1="CLOSE", LABEL_2="REG")"""

# TODO: ADX TA on SMA filtered OHL data set
