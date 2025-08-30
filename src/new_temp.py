import matplotlib.pyplot as plt
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

import numpy as np

date = Datetime("1990/05/20", "15:30", "+00:00")
pos = GeoPos("51.5074", "-0.1278")  # Лондон
chart = Chart(date, pos)

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.add_artist(plt.Circle((0,0), 1, fill=False))

# отрисовка планет
for obj in chart.objects:
    lon = chart.get(obj).lon  # долгота в зодиаке
    x = 0.9 * np.cos(np.radians(lon * 30 / 360))  # условное преобразование
    y = 0.9 * np.sin(np.radians(lon * 30 / 360))
    ax.text(x, y, obj, ha="center", va="center")

plt.axis("off")
plt.show()
