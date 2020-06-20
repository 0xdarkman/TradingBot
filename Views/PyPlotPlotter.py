import matplotlib.pyplot as plt


def plot_graphs_two_scales(X, Y_LABEL_1="Y_1", Y_LABEL_2="Y_2", COLORS_DIFF=False, **DATA_SETS):
	graphs_1 = {}
	graphs_2 = {}
	names = []
	name_str = ""

	for key in DATA_SETS:
		name = key[8:]
		names.append(name)
		if key.find('GRAPH_1_', 0, 8) != -1:
			graphs_1[name] = DATA_SETS[key]
		elif key.find('GRAPH_2_', 0, 8) != -1:
			graphs_2[name] = DATA_SETS[key]
		else:
			raise KeyError("Data set arguments must start with either 'GRAPH_1_' or 'GRAPH_2_'.")

	for i in range(len(names)):
		if i < len(names) - 1:
			name_str += names[i] + ", "
		else:
			name_str += "and " + names[i]

	fig, ax1 = plt.subplots()
	color = 'tab:red'
	ax1.set_xlabel(name_str)
	ax1.set_ylabel(ylabel=Y_LABEL_1, color=color)

	for graph in graphs_1:
		if not COLORS_DIFF:
			ax1.plot(X, graphs_1[graph], marker='o', color=color, markersize=3)
		else:
			ax1.plot(X, graphs_1[graph], marker='o', markersize=3)
	ax1.tick_params(axis='y', labelcolor=color)

	ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
	color = 'tab:blue'
	ax2.set_ylabel(ylabel=Y_LABEL_2, color=color)  # we already handled the x-label with ax1
	for graph in graphs_2:
		if not COLORS_DIFF:
			ax2.plot(X, graphs_2[graph], marker='o', color=color, markersize=3)
		else:
			ax2.plot(X, graphs_2[graph], marker='o', markersize=3)
	ax2.tick_params(axis='y', labelcolor=color)

	fig.tight_layout()  # otherwise the right y-label is slightly clipped
	plt.show()


def plot_graphs_one_scale(X, TITLE="Stock", X_LABEL="Time", Y_LABEL="Y", **DATA_SETS):
	for key in DATA_SETS:
		plt.plot(X, DATA_SETS[key], marker='o', markersize=3, label=key)

	plt.title(TITLE)
	plt.ylabel(Y_LABEL)
	plt.xlabel(X_LABEL)
	plt.legend()

	plt.show()