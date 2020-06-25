from Controllers.TAlibWrapper import *


# Bollinger Bands strategy
def BBANDS_close_diff(CLOSE_SERIES, NORMALIZED=False, ROC=False, NBDEVUP=3.0, NBDEVDN=3.0):
	BBANDS_data = BBANDS(CLOSE_SERIES, SMOOTH=True, NBDEVUP=NBDEVUP, NBDEVDN=NBDEVDN)

	if not NORMALIZED:
		DIFFcloseNupBB_data = DIFF(CLOSE_SERIES, BBANDS_data[0])[0]
		DIFFcloseNloBB_data = DIFF(BBANDS_data[2], CLOSE_SERIES)[0]
	else:
		DIFFcloseNupBB_data = DIFF(CLOSE_SERIES, BBANDS_data[0])[1]
		DIFFcloseNloBB_data = DIFF(BBANDS_data[2], CLOSE_SERIES)[1]

	for i in range(len(DIFFcloseNupBB_data)):
		if DIFFcloseNupBB_data[i] < 0.0:
			DIFFcloseNupBB_data[i] = None
		if DIFFcloseNloBB_data[i] < 0.0:
			DIFFcloseNloBB_data[i] = None

	if not ROC:
		return DIFFcloseNupBB_data, DIFFcloseNloBB_data

	for i in range(len(DIFFcloseNupBB_data) - 1, -1, -1):
		if i == 0:
			continue

		if DIFFcloseNupBB_data[i] is not None and DIFFcloseNupBB_data[i - 1] is not None:
			DIFFcloseNupBB_data[i] = ((DIFFcloseNupBB_data[i] / DIFFcloseNupBB_data[i - 1]) - 1) * 100

		if DIFFcloseNloBB_data[i] is not None and DIFFcloseNloBB_data[i - 1] is not None:
			DIFFcloseNloBB_data[i] = ((DIFFcloseNloBB_data[i] / DIFFcloseNloBB_data[i - 1]) - 1) * 100

	return DIFFcloseNupBB_data, DIFFcloseNloBB_data


used_bbands_negs = []
def BBANDS_ROC_trigger(CLOSE_SERIES, INDEXES_BACK=5):
	bbands_diffs_roc = BBANDS_close_diff(CLOSE_SERIES=CLOSE_SERIES, ROC=True, NBDEVUP=3.0, NBDEVDN=3.0)
	bbands_diff_upper_roc_sliced = bbands_diffs_roc[0][-INDEXES_BACK:]
	bbands_diff_lower_roc_sliced = bbands_diffs_roc[1][-INDEXES_BACK:]

	print(bbands_diff_upper_roc_sliced)
	print(bbands_diff_lower_roc_sliced)

	if len(used_bbands_negs) > 0:
		for neg_n in used_bbands_negs:
			if neg_n not in bbands_diff_upper_roc_sliced or neg_n not in bbands_diff_lower_roc_sliced:
				used_bbands_negs.remove(neg_n)

	sell = False
	buy = False

	for i in range(INDEXES_BACK):
		if bbands_diff_upper_roc_sliced[i] is not None:
			if bbands_diff_upper_roc_sliced[i] < 0 and bbands_diff_upper_roc_sliced[i] not in used_bbands_negs:
				sell = True
				used_bbands_negs.append(bbands_diff_upper_roc_sliced[i])
		if bbands_diff_lower_roc_sliced[i] is not None:
			if bbands_diff_lower_roc_sliced[i] < 0 and bbands_diff_lower_roc_sliced[i] not in used_bbands_negs:
				buy = True
				used_bbands_negs.append(bbands_diff_lower_roc_sliced[i])
	"""neg_upper = any(n < 0 for n in bbands_diff_upper_roc_sliced if n is not None)
	neg_lower = any(n < 0 for n in bbands_diff_lower_roc_sliced if n is not None)"""

	if sell and buy:
		return 'NONE'
	elif buy:
		return 'BUY'
	elif sell:
		return 'SELL'
	else:
		return 'NONE'


used_bbands = []
def BBANDS_trigger(CLOSE_SERIES, INDEXES_BACK=5):
	bbands_diffs = BBANDS_close_diff(CLOSE_SERIES=CLOSE_SERIES, ROC=True, NBDEVUP=3.9, NBDEVDN=3.9)
	bbands_diff_upper_sliced = bbands_diffs[0][-INDEXES_BACK:]
	bbands_diff_lower_sliced = bbands_diffs[1][-INDEXES_BACK:]

	print(bbands_diff_upper_sliced)
	print(bbands_diff_lower_sliced)

	if len(used_bbands) > 0:
		for n in used_bbands:
			if n not in bbands_diff_upper_sliced or n not in bbands_diff_lower_sliced:
				used_bbands.remove(n)

	sell = False
	buy = False

	for i in range(INDEXES_BACK):
		if bbands_diff_upper_sliced[i] is not None:
			if bbands_diff_upper_sliced[i] > 0 and bbands_diff_upper_sliced[i] not in used_bbands:
				sell = True
				used_bbands.append(bbands_diff_upper_sliced[i])
		if bbands_diff_lower_sliced[i] is not None:
			if bbands_diff_lower_sliced[i] > 0 and bbands_diff_lower_sliced[i] not in used_bbands:
				buy = True
				used_bbands.append(bbands_diff_lower_sliced[i])
	"""neg_upper = any(n < 0 for n in bbands_diff_upper_roc_sliced if n is not None)
	neg_lower = any(n < 0 for n in bbands_diff_lower_roc_sliced if n is not None)"""

	if sell and buy:
		return 'NONE'
	elif buy:
		return 'BUY'
	elif sell:
		return 'SELL'
	else:
		return 'NONE'


# MACD Signal line strategy
def MACD_NORMALIZED(CLOSE_SERIES):
	# Not working as intended
	MACD_data = MACD(CLOSE_SERIES)
	MACD_main = MACD_data[0]
	MACD_signal = MACD_data[1]

	SMA_close = SMA(CLOSE_SERIES)
	MACD_main_normalized = []
	MACD_signal_normalized = []
	for i in range(len(CLOSE_SERIES)):
		n_main = 100.0 * MACD_main[i] / CLOSE_SERIES[i]
		n_signal = 100.0 * MACD_signal[i] / CLOSE_SERIES[i]

		MACD_main_normalized.append(n_main)
		MACD_signal_normalized.append(n_signal)
	return MACD_main_normalized, MACD_signal_normalized

def MACD_signal_diff(CLOSE_SERIES, NORMALIZED=False, ROC=False):
	MACD_data = MACD(CLOSE_SERIES)
	MACD_main = MACD_data[0]
	MACD_signal = MACD_data[1]

	if not NORMALIZED:
		return DIFF(MACD_main, MACD_signal)[0]
	else:
		return DIFF(MACD_main, MACD_signal)[1]


trigger_05 = {'BUY': 0, 'SELL': 0}
def MACD_signal_normalized_trigger(CLOSE_SERIES, INDEXES_BACK=20):
	global above_05
	MACD_sig_diff = MACD_signal_diff(CLOSE_SERIES, NORMALIZED=True)
	sigdiff_sliced_long = MACD[-INDEXES_BACK:]
	sigdiff_sliced_short = MACD[-(INDEXES_BACK // 4):]

	print(sigdiff_sliced_long)

	trigger = True


	if any(n > 0.5 for n in sigdiff_sliced_long if n is not None):
		above_05 = True
	else:
		above_05 = False

	"""neg_upper = any(n < 0 for n in bbands_diff_upper_roc_sliced if n is not None)
	neg_lower = any(n < 0 for n in bbands_diff_lower_roc_sliced if n is not None)"""

	if sell and buy:
		return 'NONE'
	elif buy:
		return 'BUY'
	elif sell:
		return 'SELL'
	else:
		return 'NONE'

# TODO: BBANDS strat: when close value goes below lower BBand, wait until close rate of change starts going positive and buy,
#  then wait until close value goes above upper BBand and rate of change gets negative. If at that point you get profit - sell.
#  Else, if at any point upper BBand dips below the value of lower BBand at the time of buy, sell at the next peak above
#  the upper BBand, no matter if you get profit.

# TODO: MACD strat: when MACD signal line dips below main MACD line and reaches atleast -0.01, buy. Vice versa when
#  peaking 0.01 difference above the main value.

# TODO: try mixed BBANDS and MACD strat.

# TODO: Try mixed BBands, MACD, and ADX below/above 25 strat.

