import matplotlib
matplotlib.use("Qt5Agg")
import sys

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MPLCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        fig = Figure(figsize = (width, height), dpi = dpi)
        self.ax = fig.add_subplot(111)
        super(MPLCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        sc = MPLCanvas(self)
        sc.ax.plot([0, 1, 2], [0, 1, 4])
        self.setCentralWidget(sc)

        self.show()

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
