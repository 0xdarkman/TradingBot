import matplotlib.pyplot as plt
import datetime
import matplotlib.dates


def plot_two_graphs_two_scales(X_1, Y_1, X_2, Y_2, LABEL_1="Plot 1", LABEL_2="Plot 2", Y_LABEL_1="Plot 1", Y_LABEL_2="Plot 2"):
	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel(LABEL_1 + " and " + LABEL_2)
	ax1.set_ylabel(ylabel=Y_LABEL_1, color=color)
	ax1.plot(X_1, Y_1, marker='o', color=color, markersize=3)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
	color = 'tab:blue'
	ax2.set_ylabel(ylabel=Y_LABEL_2, color=color)  # we already handled the x-label with ax1
	ax2.plot(X_2, Y_2, marker='o', color=color, markersize=3)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()


def plot_two_graphs_one_scale(X, Y_1, Y_2, TITLE="Stock", X_LABEL="Time", Y_LABEL="Y", LABEL_1="Plot 1", LABEL_2="Plot 2"):
	color = 'tab:red'
	plt.plot(X, Y_1, marker='o', color=color, markersize=3, label=LABEL_1)

	color = 'tab:blue'
	plt.plot(X, Y_2, marker='o', color=color, markersize=3, label=LABEL_2)

	plt.title(TITLE)
	plt.ylabel(X_LABEL)
	plt.xlabel(Y_LABEL)
	plt.legend()

	plt.show()


def plot_three_graphs_one_scale(X, Y_1, Y_2, Y_3, TITLE="Stock", X_LABEL="Time", Y_LABEL="Y", LABEL_1="Plot 1", LABEL_2="Plot 2", LABEL_3="Plot 3"):
	color = 'tab:red'
	plt.plot(X, Y_1, marker='o', color=color, markersize=3, label=LABEL_1)

	color = 'tab:blue'
	plt.plot(X, Y_2, marker='o', color=color, markersize=3, label=LABEL_2)

	color = 'tab:green'
	plt.plot(X, Y_3, marker='o', color=color, markersize=3, label=LABEL_3)

	plt.title(TITLE)
	plt.ylabel(X_LABEL)
	plt.xlabel(Y_LABEL)
	plt.legend()

	plt.show()


def plot_days_evenly():
	# define the ranges for the dates
	drange = [[datetime.date(2020,6,1),datetime.date(2020,8,31)] for i in range(2000,2009)]

	# create as many subplots as there are date ranges
	fig, axes= plt.subplots(ncols=len(drange), sharey=True)
	fig.subplots_adjust(bottom=0.3,wspace=0)

	ymax = 1.1*y.max()
	# loop over subplots and limit each to one date range
	for i, ax in enumerate(axes):
		ax.set_xlim(drange[i][0],drange[i][1])
		ax.set_ylim(0,ymax)
		ax.scatter(x,y, s=4)
		loc = matplotlib.dates.MonthLocator([6,7,8])
		fmt =  matplotlib.dates.DateFormatter("%Y-%b")
		ax.xaxis.set_major_locator(loc)
		ax.xaxis.set_major_formatter(fmt)
		plt.setp(ax.get_xticklabels(), rotation=90)
		if i!=0:
			ax.tick_params(axis="y", which="both", length=0)

	plt.show()