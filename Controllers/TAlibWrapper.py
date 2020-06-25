import numpy as np
from datetime import datetime, timedelta
from talib import abstract


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

def BBANDS(DATA_LIST, PERIOD=7, SMOOTH=True, SMOOTH_PERIOD=5, NBDEVUP=2.0, NBDEVDN=2.0):
	"""
	Bollinger Bands
	:param NBDEVDN:
	:param NBDEVUP:
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return: an array of 3 arrays
	"""
	BBANDS_var = abstract.Function('BBANDS')

	np_array = np.asarray(DATA_LIST)

	BBANDS_data = BBANDS_var(np_array, timeperiod=PERIOD, nbdevup=NBDEVUP, nbdevdn=NBDEVDN)
	if not SMOOTH:
		return BBANDS_data
	else:
		return [SMA(x, PERIOD=SMOOTH_PERIOD) for x in BBANDS_data]


# Oscillators
def MACD(DATA_LIST, FASTPERIOD=12, SLOWPERIOD=26, SIGNALPERIOD=9):
	"""
	:param SIGNALPERIOD:
	:param SLOWPERIOD:
	:param FASTPERIOD:
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: three arrays of moving average convergence divergence
	"""
	MACD_var = abstract.Function('MACD')

	np_array = np.asarray(DATA_LIST)
	return MACD_var(np_array, fastperiod=FASTPERIOD, slowperiod=SLOWPERIOD, signalperiod=SIGNALPERIOD)

def RSI(DATA_LIST, PERIOD=14):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array of simple moving averages
	"""
	RSI_var = abstract.Function('RSI')

	np_array = np.asarray(DATA_LIST)
	return RSI_var(np_array, timeperiod=PERIOD)

def ULTOSC(DATA_LIST_HIGH, DATA_LIST_LOW, DATA_LIST_CLOSE, TIMEPERIOD1=7, TIMEPERIOD2=14, TIMEPERIOD3=28):
	ULTOSC_var = abstract.Function('ULTOSC')

	np_array_high = np.asarray(DATA_LIST_HIGH)
	np_array_low = np.asarray(DATA_LIST_LOW)
	np_array_close = np.asarray(DATA_LIST_CLOSE)
	return ULTOSC_var(np_array_high, np_array_low, np_array_close, timeperiod1=TIMEPERIOD1, timeperiod2=TIMEPERIOD2, timeperiod3=TIMEPERIOD3)


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

def ROCP(DATA_LIST, PERIOD=7):
	"""
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the average
	:return: array: Rate of change :  (price-prevPrice)/prevPrice

	"""
	ROC_var = abstract.Function('ROCP')

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

def STDDEV(DATA_LIST, PERIOD=5, NBDEV=1.0, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Standard Deviation
	:param NBDEV:
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	STDDEV_var = abstract.Function('STDDEV')

	np_array = np.asarray(DATA_LIST)

	STDDEV_data = STDDEV_var(np_array, timeperiod=PERIOD, nbdev=NBDEV)
	if not SMOOTH:
		return STDDEV_data
	else:
		return SMA(STDDEV_data, PERIOD=SMOOTH_PERIOD)

def VAR(DATA_LIST, PERIOD=5, NBDEV=1.0, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Standard Deviation
	:param NBDEV:
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	VAR_var = abstract.Function('VAR')

	np_array = np.asarray(DATA_LIST)

	VAR_data = VAR_var(np_array, timeperiod=PERIOD, nbdev=NBDEV)
	if not SMOOTH:
		return VAR_data
	else:
		return SMA(VAR_data, PERIOD=SMOOTH_PERIOD)

def TSF(DATA_LIST, PERIOD=14, SMOOTH=False, SMOOTH_PERIOD=7):
	"""
	Standard Deviation
	:param DATA_LIST: list/array of numbers
	:param PERIOD: integer: the number of values that is used to calculate the ADX values
	:param SMOOTH: bool: set to True to smooth the ADX by using SMA
	:param SMOOTH_PERIOD: the number of values that is used to calculate the SMA
	:return:
	"""
	TSF_var = abstract.Function('TSF')

	np_array = np.asarray(DATA_LIST)

	TSF_data = TSF_var(np_array, timeperiod=PERIOD)
	if not SMOOTH:
		return TSF_data
	else:
		return SMA(TSF_data, PERIOD=SMOOTH_PERIOD)


# Other
def DIFF(DATA_LIST_1, DATA_LIST_2):
	array_1 = DATA_LIST_1.copy()
	array_2 = DATA_LIST_2.copy()

	len_1 = len(array_1)
	len_2 = len(array_2)
	max_len = max(len_1, len_2)
	if len_1 < max_len:
		for i in range(max_len - len_1):
			array_1.insert(0, 0)
	elif len_2 < max_len:
		for i in range(max_len - len_2):
			array_2.insert(0, 0)

	diff_array = []
	diff_pct_array = []
	for idx in range(len(array_1)):
		elem_1 = array_1[idx]
		elem_2 = array_2[idx]

		diff = elem_1 - elem_2
		diff_pct = round(((elem_1 - elem_2) / elem_2), 3)

		diff_array.append(diff)
		diff_pct_array.append(diff_pct)

	max_diff = np.nanmax(diff_array)
	min_diff = np.nanmin(diff_array)
	min_diff = -max_diff
	normal_diff_array = []
	for i in diff_array:
		n = ((i - min_diff) / (max_diff - min_diff) * 2) - 1
		normal_diff_array.append(n)

	return diff_array, normal_diff_array, diff_pct_array

def SERIES_CUTOFF(TIME_SERIES, VALUE_SERIES, TYPE_OF_INDEX='DATETIME', N_HOURS=8):
	if TYPE_OF_INDEX == 'DATETIME':
		now = datetime.now()
		if now > datetime(now.year, now.month, now.day, 16, 25):
			now = datetime(now.year, now.month, now.day, 16, 25)
		elif now < datetime(now.year, now.month, now.day, 9, 0):
			now = datetime(now.year, now.month, now.day - 1, 16, 25)

		hours_left = N_HOURS
		while hours_left > 0:
			now -= timedelta(hours=1)
			hours_left -= 1

			if now.hour < 9:
				diff_mins = 60 - now.minute
				now = datetime(now.year, now.month, now.day - 1, 16, 25)
				now -= timedelta(minutes=diff_mins)

		found_tick = False
		while not found_tick:
			try:
				time_series = TIME_SERIES[TIME_SERIES.index(datetime(now.year,
				                                                     now.month,
				                                                     now.day,
				                                                     now.hour,
				                                                     now.minute)):]
				found_tick = True
			except IndexError:
				now -= timedelta(minutes=1)

		value_series = VALUE_SERIES[len(TIME_SERIES) - len(time_series):]

	return time_series, value_series