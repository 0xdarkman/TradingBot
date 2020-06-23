import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import OrderedDict
from random import randint
from datetime import datetime


def plot_line_sets(X, **DATA_SETS):
	"""

	:param X: list/array: x axis data
	:param DATA_SETS: list
	:keyword GRAPH_(int)_NAME={'PLOT': [1, 2, 3, ...], 'COLOR': 'red', 'DASH': 'dot', 'Y_AXIS': 'y axis name'}]
	:return:
	"""
	named_colorscales = ['aliceblue', 'aqua', 'aquamarine', 'azure',
	                     'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
	                     'blueviolet', 'brown', 'burlywood', 'cadetblue',
	                     'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
	                     'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
	                     'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
	                     'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
	                     'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
	                     'darkslateblue', 'darkslategray', 'darkslategrey',
	                     'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
	                     'dodgerblue', 'firebrick',
	                     'forestgreen', 'fuchsia', 'gainsboro',
	                     'gold', 'goldenrod', 'green',
	                     'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
	                     'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
	                     'lemonchiffon', 'lime', 'limegreen',
	                     'linen', 'magenta', 'maroon', 'mediumaquamarine',
	                     'mediumblue', 'mediumorchid', 'mediumpurple',
	                     'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
	                     'mediumturquoise', 'mediumvioletred', 'midnightblue',
	                     'mintcream', 'mistyrose', 'moccasin', 'navy',
	                     'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
	                     'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
	                     'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
	                     'plum', 'powderblue', 'purple', 'red', 'rosybrown',
	                     'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
	                     'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
	                     'skyblue', 'slateblue', 'slategrey', 'snow',
	                     'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
	                     'turquoise', 'violet', 'wheat',
	                     'yellow', 'yellowgreen']

	graphs = OrderedDict([])
	names = []
	name_str = ""

	for key in DATA_SETS:
		name = key[8:]
		names.append(name)
		if key[:6] == 'GRAPH_':
			subplot = int(key[6])

			if subplot not in graphs:
				graphs[subplot] = OrderedDict([])
			graphs[subplot][name] = DATA_SETS[key]
		else:
			raise KeyError("Data set arguments must start with 'GRAPH_'.")

	num_of_subplots = len(graphs.keys())

	fig = go.Figure()
	if num_of_subplots == 1:
		layout_args = {'yaxis': dict(
			title=graphs[1][next(iter(graphs[1]))]['Y_AXIS'])}
		fig.update_layout(layout_args)
	if num_of_subplots == 2:
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		layout_args = {'yaxis': dict(
			title=graphs[1][next(iter(graphs[1]))]['Y_AXIS']),
					   'yaxis2': dict(
			title=graphs[2][next(iter(graphs[2]))]['Y_AXIS'])}
		fig.update_layout(layout_args)

	elif num_of_subplots > 4:
		raise ValueError("Max 4 subplots are supported.")
	elif num_of_subplots > 2:
		# DOESNT WORK
		layout_args = {}
		for y_axis in range(1, num_of_subplots + 1):
			color = named_colorscales[randint(0, len(named_colorscales) - 1)]
			side = ''
			if y_axis % 2 == 0:
				side = "right"
			else:
				side = "left"

			print(next(iter(graphs[y_axis]))['Y_AXIS'])
			layout_args['yaxis' + str(y_axis)] = dict(
				title=next(iter(graphs[y_axis]))['Y_AXIS'],
				titlefont=dict(color=color),
				tickfont=dict(color=color),
				anchor="free",
				overlaying="y",
				side=side)
		fig.update_layout(**layout_args)

	# Create and style traces
	for subplot in graphs:
		for plot in graphs[subplot]:
			name = plot.replace('_', ' ')
			colors_len = len(named_colorscales)
			plot_args = dict(x=X,
			                 y=graphs[subplot][plot]['PLOT'],
			                 name=name,
			                 line=dict(color=named_colorscales[randint(0, len(named_colorscales) - 1)], width=2.5, dash='solid'),
			                 mode='lines',
			                 yaxis='y' + str(subplot)
			                 )

			# Check for dash arg
			# dash options include 'solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot'
			if 'DASH' not in graphs[subplot][plot]:
				pass
			elif graphs[subplot][plot]['DASH'] != 'none':
				plot_args['line']['dash'] = graphs[subplot][plot]['DASH']

			# Check for color arg
			if 'COLOR' not in graphs[subplot][plot] or graphs[subplot][plot]['COLOR'] == 'none':
				pass
			else:
				plot_args['line']['color'] = graphs[subplot][plot]['COLOR']

			if 'Y_AXIS' not in graphs[subplot][plot]:
				pass

			if 'MODE' in graphs[subplot][plot]:
				if graphs[subplot][plot]['MODE'] != 'none':
					plot_args['mode'] = graphs[subplot][plot]['MODE']

			fig.add_trace(go.Scatter(plot_args))

	if isinstance(X[0], datetime):
		days_list = []
		for date_idx in range(1, len(X)):
			day_stop = datetime(X[date_idx].year, X[date_idx].month, X[date_idx].day, 16, 26)
			day_start = datetime(X[date_idx].year, X[date_idx].month, X[date_idx].day + 1, 9, 0)
			if day_stop.weekday() == 4:
				day_start = datetime(X[date_idx].year, X[date_idx].month, X[date_idx].day + 3, 9, 0)
			day_array = [day_stop, day_start]
			if day_array not in days_list:
				days_list.append(day_array)

		rangebreaks = [dict(bounds=x) for x in days_list]
		fig.update_xaxes(rangebreaks=rangebreaks)

	# Edit the layout
	for idx in range(len(names)):
		name = names[idx].replace('_', ' ')
		if idx != len(names) - 1:
			name_str += name + ", "
		else:
			name_str += name
	fig.update_layout(title=name_str,
	                  xaxis_title='Time')

	fig.show()