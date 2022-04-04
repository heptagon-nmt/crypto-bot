from datetime import datetime, timedelta
from ML_predictor_backend import *
from get_data import *
import sys
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QPalette, QRegularExpressionValidator
from PySide6.QtWidgets import (QApplication, QPushButton, QComboBox,
    QFormLayout, QGridLayout, QLabel, QLineEdit, QListWidget, QMainWindow, 
    QMessageBox, QToolBar, QWidget)
import pyqtgraph as pg

models = ["random_forest", "linear", "lasso", "gradient_boosting", "bagging", "ridge"]
lineEditValidator = QRegularExpressionValidator(r"[1-9][0-9]*")

def format_intervals(intervals):
    """
    :param list[int] intervals: The list of available intervals (in minutes) for a given API
    :return: String-formatted intervals for better readability
    :rtype: list[int]
    """
    new_intervals = []
    for interval in intervals:
        new_intervals.append(str(timedelta(minutes = interval)))
    return new_intervals

class MainWindow(QMainWindow):
    """
    This window contains only the CentralWidget, which itself contains all of 
    the important subwidgets.

    Attributes:
        centralWidget       The widget to contain all other widgets
        fileMenu            The "File" tab at the top left
    """
    def __init__(self):
        super().__init__()

        toolBar = QToolBar()
        self.addToolBar(toolBar)
        fileMenu = self.menuBar().addMenu("&File")
        editMenu = self.menuBar().addMenu("&Edit")
        exitAction = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        self.centralWidget = CentralWidget()
        self.setCentralWidget(self.centralWidget)
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        # Create a palette that looks nice. Dark mode, maybe?
        #self.createPalette()

    def load(self):
        QMessageBox.warning(self, "AxViewer", f"Unable to load the veendow.")

    def createPalette(self):
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, "#636e72")
        self.palette.setColor(QPalette.WindowText, "#dddeee")
        self.palette.setColor(QPalette.Base, "#2d3436")
        self.palette.setColor(QPalette.Text, "#ffffff")
        self.setPalette(self.palette)
class CentralWidget(QWidget):
    """
    This is the widget to contain the APIWindow, MLWindow, as well as 
    AnalyticsWindow and GraphsWindow.

    Attributes:
        gridLayout      
    """
    def __init__(self):
        super().__init__()
        self.gridLayout = QGridLayout(self)

        self.apiWindow = APIWindow()
        self.modelWindow = MLWindow()
        self.modelWindow.trainButton.clicked.connect(self._getForecast)
        self.analyticsWindow = AnalyticsWindow()
        
        self.gridLayout.addWidget(self.apiWindow, 0, 0)
        self.gridLayout.addWidget(self.modelWindow, 0, 1)
        self.gridLayout.addWidget(self.analyticsWindow, 0, 2)
    def _getForecast(self):
        data = self.apiWindow.getData()
        if data is None:
            return
        print(data)

class APIWindow(QWidget):
    """
    This is the leftmost section of the main window that allows the user to 
    select the data parameters, such as API source, range, and intervals.
    """
    def __init__(self):
        super().__init__()
        self._getSymbolListsAndInfo()

        formLayout = QFormLayout(self)
        self.sourceComboBox = QComboBox()
        self.sourceComboBox.addItems(sources_list)
        self.sourceComboBox.currentIndexChanged.connect(self._sourceChangeMethod)
        self.symbolFilter = QLineEdit()
        self.symbolFilter.setPlaceholderText("ID (e.g. ethereum)")
        self.symbolFilter.textChanged.connect(self.populateSymbols)
        self.symbolListWidget = QListWidget()
        self.symbolListWidget.itemSelectionChanged.connect(self.updateSelected)
        # Magic number 5 since IDK how to properly set widget sizes 
        self.symbolListWidget.setMinimumWidth(5 * max(len(item) for item in self.ids["coingecko"]))
        self.selectedSymbol = QLabel()
        self.intervalComboBox = QComboBox()
        self.rangeEdit = QLineEdit()
        self.rangeEdit.setText("20")
        self.rangeEdit.setPlaceholderText("Number of days behind the current to collect data.")
        self.rangeEdit.setValidator(lineEditValidator)
        self.rangeEdit.textEdited.connect(self._setAvailableIntervals)
        self.errLabel = QLabel()

        formLayout.addRow("API Source:", self.sourceComboBox)
        formLayout.addRow("Symbol:", self.symbolFilter)
        formLayout.addRow("", self.symbolListWidget)
        formLayout.addRow("Selected Symbol:", self.selectedSymbol)
        formLayout.addRow("Range (in days):", self.rangeEdit)
        formLayout.addRow("Interval:", self.intervalComboBox)
        formLayout.addRow("", self.errLabel)
        self._sourceChangeMethod()
    def populateSymbols(self):
        source = self.sourceComboBox.currentText()
        search = self.symbolFilter.text()
        displayedSymbols = [symbol for symbol in self.ids[source] 
                                if search.upper() in symbol.upper()]
        self.symbolListWidget.clear()
        self.symbolListWidget.addItems(displayedSymbols)
    def _setAvailableIntervals(self):
        """
        Set intervals based on the API source, and the range (in the case of
        CoinGecko).

        :return: None
        """
        source = self.sourceComboBox.currentText()
        intervals = self.intervals[source]
        range_str = self.rangeEdit.text()
        if len(range_str) > 0:
            range_val = abs(int(range_str))
            if source == "coingecko":
                if 1 <= range_val <= 2: index = 0
                elif 2 < range_val <= 30: index = 1
                elif range_val > 30: index = 2
                else: 
                    index = 0
                intervals = [intervals[index]]
            self.intervalComboBox.clear()
            self.intervalComboBox.addItems(intervals)

    def updateSelected(self):
        selectedItem = self.symbolListWidget.currentItem()
        if selectedItem is not None:
            self.selectedSymbol.setText(selectedItem.text())
    def _sourceChangeMethod(self):
        self.populateSymbols()
        self._setAvailableIntervals()
    def _getSymbolListsAndInfo(self):
        self.api_dict = {"coingecko": CoinGecko(), "kraken": Kraken(), "cmc": CMC()}
        self.ids = dict(zip(sources_list, [api.get_ids() for api in list(self.api_dict.values())]))
        self.intervals = dict(zip(sources_list, [format_intervals(api.get_intervals()) for api in list(self.api_dict.values())]))
    def getData(self):
        source = self.sourceComboBox.currentText()
        symbolWidget = self.symbolListWidget.currentItem()
        if symbolWidget == None:
            self.errLabel.setText("Must select a symbol.")
            return
        symbol = symbolWidget.text()
        rangeVal = self.rangeEdit.text()
        if len(rangeVal) == 0:
            self.errLabel.setText("Range must be at least 1.")
            return
        rangeVal = int(rangeVal)
        # We only need the interval values for Kraken since the intervals for other APIs are fixed. 
        self.errLabel.setText("")
        intervalString = self.intervalComboBox.currentText()
        if len(intervalString) > 7: 
            interval = int(intervalString.split()[0]) * 24 * 60
        else:
            dt = datetime.strptime(intervalString, "%H:%M:%S")
            td = timedelta(hours = dt.hour, minutes = dt.minute, seconds = dt.second)
            interval = int(td.seconds / 60)
            print("Interval %d" % interval)
        if source == "kraken":
            data = np.array(self.api_dict[source].get_ohlc(symbol, "USD", rangeVal, interval))
        if source == "coingecko":
            data = self.api_dict[source].get_opening_price(symbol, "USD", rangeVal)
        if source == "cmc":
            data = self.api_dict[source].get_opening_price(symbol)
        return data
        # If all API inputs are correct then unset text from errLabel

class MLWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = QFormLayout(self)
        self.modelComboBox = QComboBox()
        self.modelComboBox.addItems(models)
        self.modelComboBox.currentIndexChanged.connect(self._modelChanged)
        self.lagsLineEdit = QLineEdit()
        #self.lagsLineEdit.setPlaceholderText("Skforecast hyperparameter for time series")
        self.lagsLineEdit.setValidator(lineEditValidator)
        self.nEstimatorsLineEdit = QLineEdit()
        self.nEstimatorsLineEdit.setValidator(lineEditValidator)
        #self.nEstimatorsLineEdit.setPlaceholderText("Number of decision trees in random forest")
        self.maxDepthLineEdit = QLineEdit()
        self.maxDepthLineEdit.setValidator(lineEditValidator)
        #self.maxDepthLineEdit.setPlaceholderText("Maximum depth of tree")
        self.maxIterLineEdit = QLineEdit()
        self.maxIterLineEdit.setValidator(lineEditValidator)
        #self.maxIterLineEdit.setPlaceholderText("Applied to lasso and ridge models")
        self.trainButton = QPushButton("Forecast")
        self.formLayout.addRow("Regression Model:", self.modelComboBox)
        self.formLayout.addRow("Lags:", self.lagsLineEdit)
        self.formLayout.addRow("Number of Estimators:", self.nEstimatorsLineEdit)
        self.formLayout.addRow("Max Depth:", self.maxDepthLineEdit)
        self.formLayout.addRow("Max Iterations:", self.maxIterLineEdit)
        self.formLayout.addRow("", self.trainButton)
        self._modelChanged()
    def _modelChanged(self):
        model = self.modelComboBox.currentText()
        if model == "random_forest" or model == "gradient_boosting":
            self.nEstimatorsLineEdit.setEnabled(True)
            self.maxDepthLineEdit.setEnabled(True)
            self.maxIterLineEdit.setEnabled(False)
        elif model == "linear":
            self.nEstimatorsLineEdit.setEnabled(False)
            self.maxDepthLineEdit.setEnabled(False)
            self.maxIterLineEdit.setEnabled(False)
        elif model == "lasso" or model == "ridge":
            self.nEstimatorsLineEdit.setEnabled(False)
            self.maxDepthLineEdit.setEnabled(False)
            self.maxIterLineEdit.setEnabled(True)
        elif model == "bagging":
            self.nEstimatorsLineEdit.setEnabled(True)
            self.maxDepthLineEdit.setEnabled(False)
            self.maxIterLineEdit.setEnabled(False)

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.formLayout = QFormLayout(self)
        self.forecastedPricesListWidget = QListWidget()
        self.forecastedPricesListWidget.setMinimumWidth(300)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground("w")
        self.graphWidget.setMinimumWidth(self.graphWidget.height())
        self.formLayout.addRow("", self.graphWidget)
        self.formLayout.addRow("Forecast (USD):", self.forecastedPricesListWidget)
    def plot(self, x, y):
        self.graphWidget.plot(x, y, pen = (0, 0, 255), name = "Predicted Prices")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
    mainWin.show()
    sys.exit(app.exec())
