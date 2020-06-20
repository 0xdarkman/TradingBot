import numpy as np
from talib import abstract
from Views import PyPlotPlotter
from Scrapers import NordnetScraper

# Functions used in this wrapper.
# Set them in front so that they load on import.

# Averages
SMA_var = abstract.Function('SMA')
WMA_var = abstract.Function('WMA')
EMA_var = abstract.Function('EMA')
DEMA_var = abstract.Function('DEMA')
TEMA_var = abstract.Function('TEMA')

# Momentum Indicators
ADX_var = abstract.Function('ADX')
ROC_var = abstract.Function('ROC')
MOM_var = abstract.Function('MOM')

# Regression
SLOPE_REG_var = abstract.Function('LINEARREG_SLOPE')
STDDEV_var = abstract.Function('STDDEV')

# Other
BBANDS_var = abstract.Function('BBANDS')


# Averages
def SMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of simple moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return SMA_var(np_array, timeperiod=PERIOD)


def WMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of weighted moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return WMA_var(np_array, timeperiod=PERIOD)


def EMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of exponential moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return EMA_var(np_array, timeperiod=PERIOD)


def DEMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of double exponential moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return DEMA_var(np_array, timeperiod=PERIOD)


def TEMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of triple exponential moving averages
	"""
	np_array = np.asarray(DATA_LIST)
	return TEMA_var(np_array, timeperiod=PERIOD)


# Momentum Indicators
def ADX(DATA_LIST_OPEN, DATA_LIST_HIGH, DATA_LIST_LOW, PERIOD=21, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Average Directional Movement Index
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

	ADX_data = ADX_var(np_array_open, np_array_high, np_array_low, timeperiod=PERIOD)
	if not SMOOTH:
		return ADX_data
	else:
		return SMA(ADX_data, PERIOD=SMOOTH_PERIOD)


def ROC(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array: Rate of change : ((price/prevPrice)-1)*100

	"""
	np_array = np.asarray(DATA_LIST)
	return ROC_var(np_array, timeperiod=PERIOD)


def MOM(DATA_LIST, PERIOD=7):
	"""
	Momentum
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array: Momentum

	"""
	np_array = np.asarray(DATA_LIST)
	return MOM_var(np_array, timeperiod=PERIOD)


# Regression
def SLOPE_REG(DATA_LIST, PERIOD=5, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Linear Regression Slope
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	np_array = np.asarray(DATA_LIST)

	SLOPE_REG_data = SLOPE_REG_var(np_array, timeperiod=PERIOD)
	if not SMOOTH:
		return SLOPE_REG_data
	else:
		return SMA(SLOPE_REG_data, PERIOD=SMOOTH_PERIOD)


def STDDEV(DATA_LIST, PERIOD=5, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Standard Deviation
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	np_array = np.asarray(DATA_LIST)

	STDDEV_data = STDDEV_var(np_array, timeperiod=PERIOD)
	if not SMOOTH:
		return STDDEV_data
	else:
		return SMA(STDDEV_data, PERIOD=SMOOTH_PERIOD)


# Other
def BBANDS(DATA_LIST, PERIOD=7, SMOOTH=True, SMOOTH_PERIOD=5):
	"""
	Bollinger Bands
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return: an array of 3 arrays
	"""
	np_array = np.asarray(DATA_LIST)
	BBANDS_data = BBANDS_var(np_array, timeperiod=PERIOD)
	if not SMOOTH:
		return BBANDS_data
	else:
		return [SMA(x, PERIOD=SMOOTH_PERIOD) for x in BBANDS_data]


series = next(iter((NordnetScraper.main(GET_SERIES='SINGLE', TICKER='ENDUR', PERIOD='2d')).values()))
time_series = series['TIME']
open_series = series['OPEN']
high_series = series['HIGH']
low_series = series['LOW']
close_series = series['CLOSE']
volume_series = series['VOLUME']

BBANDS_data = BBANDS(close_series, SMOOTH=True)
ADX_data = ADX(open_series, high_series, low_series, PERIOD=10, SMOOTH=True)
WMA_data = WMA(close_series)
SMA_data = SMA(close_series)
EMA_data = EMA(close_series)

PyPlotPlotter.plot_graphs_one_scale(time_series, X_LABEL="Time", Y_LABEL="NOK",
                                    BBAND_upper=BBANDS_data[0], BBAND_lower=BBANDS_data[2], WMA=WMA_data, CLOSE=close_series)

"""PyPlotPlotter.plot_graphs_two_scales(time_series, Y_LABEL_1="NOK", Y_LABEL_2="ADX", COLORS_DIFF=False,
                                     GRAPH_1_BBAND_upper=BBANDS_data[0], GRAPH_1_BBAND_lower=BBANDS_data[2],
                                     GRAPH_1_WMA=WMA_data,
                                     GRAPH_2_ADX=ADX_data)"""

"""PyPlotPlotter.plot_two_graphs_one_scale(np.asarray(series['TIME']), np.asarray(series['CLOSE']), SMA_data,
                                        X_LABEL="Time", Y_LABEL="NOK",
                                        LABEL_1="Close data", LABEL_2="SMA21")"""

"""PyPlotPlotter.plot_three_graphs_one_scale(time_series, close_series, BBANDS_data[0], BBANDS_data[2],
                                          X_LABEL="Time", Y_LABEL="Nok",
                                          LABEL_1="CLOSE", LABEL_2="BBAND upper", LABEL_3="BBAND lower")"""
