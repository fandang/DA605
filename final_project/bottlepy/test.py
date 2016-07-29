import sqlite3
from bottle import route, install, template, run, view, Bottle
from bottle_sqlite import SQLitePlugin

import numpy as np
import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

filename = "ff_img.png"
x = np.arange(-10,10,0.1)  # Calculation
y = x**3 + 2*x**2 - 5
fig = Figure()  # Plotting
canvas = FigureCanvas(fig)
ax = fig.add_subplot(211)
ax.plot(x, y)
ax.set_title('Plot by Matplotlib')
ax.grid(True)
ax.set_xlabel('x')
ax.set_ylabel('y')
canvas.print_figure(filename)
