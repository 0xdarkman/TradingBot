import json
import os.path
import matplotlib.pyplot as plt

with open("test.json") as json_file:
	json_stock = json.load(json_file)

print(json_stock["chart"]["result"][0]["timestamp"])

plt.plot(json_stock["chart"]["result"][0]["timestamp"], json_stock["chart"]["result"][0]["indicators"]["quote"][0]["high"])
plt.show()