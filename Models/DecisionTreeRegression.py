from Scrapers import scraper1
from sklearn import tree
import matplotlib.pyplot as plt

training_data = scraper1.get_processed_intraday_OSE("SAS+NOK", DATE="2020-06-10")
test_data = scraper1.get_processed_intraday_OSE("SAS+NOK")

train_x, train_y = training_data['x_axis'], training_data['y_axis']
test_x, test_y = test_data['x_axis'], test_data['y_axis']


train_matrix = []
for idx in range(len(train_x)):
	train_matrix.append([idx, train_y[idx]])

test_matrix = []
for idx in range(len(test_x)):
	test_matrix.append([idx, test_y[idx]])

train_x = [x[0] for x in train_matrix]
test_x = [x[0] for x in test_matrix]

regr_1 = tree.DecisionTreeClassifier(max_depth=2)
regr_2 = tree.DecisionTreeClassifier(max_depth=5)
regr_3 = tree.DecisionTreeClassifier(max_depth=100)

regr_1.fit(train_matrix, train_y)
regr_2.fit(train_matrix, train_y)
regr_3.fit(train_matrix, train_y)

y_1 = regr_1.predict(test_matrix)
y_2 = regr_2.predict(test_matrix)
y_3 = regr_3.predict(test_matrix)

plt.figure()
plt.scatter(test_x, test_y, s=20, edgecolor="black",
            c="darkorange", label="data")
plt.plot(test_x, y_1, color="cornflowerblue",
         label="max_depth=2", linewidth=2)
plt.plot(test_x, y_2, color="yellowgreen", label="max_depth=5", linewidth=2)
plt.plot(test_x, y_3, color="violet", label="max_depth=None", linewidth=2)
plt.xlabel("data")
plt.ylabel("target")
plt.title("Decision Tree Regression")
plt.legend()

plt.show()