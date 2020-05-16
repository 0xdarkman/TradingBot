import scraper

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


# csvFile = scraper.array2csv_file("NORDNET")
df = scraper.read_csv("NORDNET_1589593909.csv", 15)

df.plot(kind='bar', x='NAME', y='CHANGE_%',color='red')
plt.show()