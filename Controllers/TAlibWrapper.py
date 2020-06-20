import numpy as np
from talib import abstract
from Views import PyPlotPlotter
from Scrapers import NordnetScraper


# Averages
def SMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of simple moving averages
	"""
	SMA_var = abstract.Function('SMA')

	np_array = np.asarray(DATA_LIST)
	return SMA_var(np_array, timeperiod=PERIOD)
def WMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of weighted moving averages
	"""
	WMA_var = abstract.Function('WMA')

	np_array = np.asarray(DATA_LIST)
	return WMA_var(np_array, timeperiod=PERIOD)
def EMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of exponential moving averages
	"""
	EMA_var = abstract.Function('EMA')

	np_array = np.asarray(DATA_LIST)
	return EMA_var(np_array, timeperiod=PERIOD)
def DEMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of double exponential moving averages
	"""
	DEMA_var = abstract.Function('DEMA')

	np_array = np.asarray(DATA_LIST)
	return DEMA_var(np_array, timeperiod=PERIOD)
def TEMA(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of triple exponential moving averages
	"""
	TEMA_var = abstract.Function('TEMA')

	np_array = np.asarray(DATA_LIST)
	return TEMA_var(np_array, timeperiod=PERIOD)
def MACD(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: three arrays of moving average convergence divergence
	"""
	MACD_var = abstract.Function('MACD')

	np_array = np.asarray(DATA_LIST)
	return MACD_var(np_array, timeperiod=PERIOD)

# Momentum Indicators
def ADX(DATA_LIST_HIGH, DATA_LIST_LOW, DATA_LIST_CLOSE, PERIOD=21, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Average Directional Movement Index
	:param DATA_LIST_HIGH: list/array of numbers: period high values
	:param DATA_LIST_LOW: list/array of numbers: period low values
	:param DATA_LIST_CLOSE: list/array of numbers: period close values
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return: array of ADX values
	"""
	ADX_var = abstract.Function('ADX')

	np_array_high = np.asarray(DATA_LIST_HIGH)
	np_array_low = np.asarray(DATA_LIST_LOW)
	np_array_close = np.asarray(DATA_LIST_CLOSE)

	ADX_data = ADX_var(np_array_high, np_array_low, np_array_close, timeperiod=PERIOD)
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
	ROC_var = abstract.Function('ROC')

	np_array = np.asarray(DATA_LIST)
	return ROC_var(np_array, timeperiod=PERIOD)
def MOM(DATA_LIST, PERIOD=7):
	"""
	Momentum
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array: Momentum

	"""
	MOM_var = abstract.Function('MOM')

	np_array = np.asarray(DATA_LIST)
	return MOM_var(np_array, timeperiod=PERIOD)

# Regression
def SLOPE_REG(DATA_LIST, PERIOD=5, SMOOTH=False, SMOOTH_PERIOD=5):
	"""
	Linear Regression Slope
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	SLOPE_REG_var = abstract.Function('LINEARREG_SLOPE')

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
	STDDEV_var = abstract.Function('STDDEV')

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
	BBANDS_var = abstract.Function('BBANDS')

	np_array = np.asarray(DATA_LIST)

	BBANDS_data = BBANDS_var(np_array, timeperiod=PERIOD)
	if not SMOOTH:
		return BBANDS_data
	else:
		return [SMA(x, PERIOD=SMOOTH_PERIOD) for x in BBANDS_data]
