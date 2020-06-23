from Controllers.TAlibWrapper import *


def evaluate_time_series_BBANDS(X, CLOSE_SERIES, PERIOD=7):
	hey = 1


# TODO: BBANDS strat: when close value goes below lower BBand, wait until close rate of change starts going positive and buy,
#  then wait until close value goes above upper BBand and rate of change gets negative. If at that point you get profit - sell.
#  Else, if at any point upper BBand dips below the value of lower BBand at the time of buy, sell at the next peak above
#  the upper BBand, no matter if you get profit.

# TODO: MACD strat: when MACD signal line dips below main MACD line and reaches atleast -0.01, buy. Vice versa when
#  peaking 0.01 difference above the main value.

# TODO: try mixed BBANDS and MACD strat.

