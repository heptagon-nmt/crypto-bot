from datetime import datetime, timedelta

from numpy import full
from src.ML_predictor_backend import *
from src.get_data import *
import sys
from PySide6 import QtWidgets
from PySide6.QtGui import QAction, QColor, QPalette, QRegularExpressionValidator
from PySide6.QtWidgets import (QApplication, QPushButton, QCheckBox, QComboBox,
    QHBoxLayout, QFormLayout, QGridLayout, QLabel, QLineEdit, QListWidget, QMainWindow, 
    QMessageBox, QTabWidget, QToolBar, QWidget)
import pyqtgraph as pg
from typing import List

models = ["random_forest", "linear", "lasso", "gradient_boosting", "bagging", "ridge"]
max_layers = 5
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
def get_comma_separated_list(array):
    """
    Return a comma separated string of elements in an array
    """
    return "".join("{}, ".format(val) for val in list(array))[:-2]

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
        self.tabWindow = QTabWidget()
        self.centralWidget = CentralWidget()
        self.classificationWindow = ClassificationWindow()
        self.classificationWindow.nnWindow.trainButton.clicked.connect(self.train)
        self.tabWindow.addTab(self.centralWidget, "Spot Price Forecasting")
        self.tabWindow.addTab(self.classificationWindow, "Color Prediction")
        fileMenu = self.menuBar().addMenu("&File")
        editMenu = self.menuBar().addMenu("&Edit")
        viewMenu = self.menuBar().addMenu("&View")
        exitAction = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        fullScreenAction = QAction("&Fullscreen", self, shortcut="F11", triggered = self.maximize)
        savePlotAction = QAction("&Save Plot", self, shortcut="Ctrl+S", triggered = self.savePlot)
        nextTabAction = QAction("&Next Tab", self, shortcut="Ctrl+Tab", triggered = self.nextTab)
        prevTabAction = QAction("&Prev Tab", self, shortcut="Ctrl+Shift+Tab", triggered = self.prevTab)
        closeTabAction = QAction("&Close Tab", self, shortcut="Ctrl+W", triggered = self.closeTab)
        fileMenu.addAction(savePlotAction)
        fileMenu.addAction(exitAction)
        viewMenu.addAction(fullScreenAction)
        self.centralWidget.addAction(fullScreenAction)
        self.centralWidget.addAction(savePlotAction)
        self.centralWidget.addAction(nextTabAction)
        self.centralWidget.addAction(prevTabAction)
        self.centralWidget.addAction(closeTabAction)
        self.setCentralWidget(self.tabWindow)
        self.maximized = False
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        # Create a palette that looks nice. Dark mode, maybe?
        self.createPalette()
    def load(self):
        QMessageBox.warning(self, "AxViewer", f"Unable to load the veendow.")
    def nextTab(self):
        self.centralWidget.nextTab()
    def prevTab(self):
        self.centralWidget.prevTab()
    def closeTab(self):
        self.centralWidget.closeTab()
    def createPalette(self):
        self.palette = QPalette()
        """self.palette.setColor(QPalette.Window, "#2e3440")
        self.palette.setColor(QPalette.WindowText, "#eceff4")
        self.palette.setColor(QPalette.Base, "#3b4252")
        self.palette.setColor(QPalette.AlternateBase, "#434c5e")
        self.palette.setColor(QPalette.ToolTipBase, "#4c566a")
        self.palette.setColor(QPalette.PlaceholderText, "#d8dee9")
        self.palette.setColor(QPalette.Text, "#eceff4")
        self.palette.setColor(QPalette.Button, "#5e81ac")
        self.palette.setColor(QPalette.ButtonText, "#4c566a")
        self.palette.setColor(QPalette.BrightText, "#81a1c1")"""
        self.palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.Text, QColor(255, 255, 255))
        self.palette.setColor(QPalette.Button, QColor(63, 63, 63))
        self.palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.BrightText, QColor(23, 23, 200))
        self.palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(self.palette)
    def maximize(self):
        if self.maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.maximized = not self.maximized
    def savePlot(self):
        # TODO : Finish adding this function. Ideally open a filesystem window 
        # which prompts for the path and name of the plot, as well as the file
        # extension.
        print("To be added later...")
    def train(self):
        """
        Get OHLC data from selected API with the following fields: (Open, High, Low, Close, Volume)
        """
        pass

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
        self.modelWindow.forecastButton.clicked.connect(self._getForecast)
        self.forecastTabWindow = ForecastTab()
        self.forecastTabWindow.setVisible(False)
        self.tabs = []
        self.gridLayout.addWidget(self.apiWindow, 0, 0)
        self.gridLayout.addWidget(self.modelWindow, 0, 1)
        self.gridLayout.addWidget(self.forecastTabWindow, 0, 2)
    def _getForecast(self):
        data = self.apiWindow.getData()
        print(data)
        interval = self.apiWindow.getInterval()
        symbol = self.apiWindow.getSymbol()
        if data is None:
            return
        forecast = self.modelWindow.getPrediction(data)
        if forecast is None:
            return
        if not self.forecastTabWindow.isVisible():
            self.forecastTabWindow.setVisible(True)
        model = self.modelWindow.getModel()
        hyperparameters = self.modelWindow.getHyperparameters()
        analyticsTab = AnalyticsWindow(symbol, model, interval, hyperparameters)
        self.tabs.append(analyticsTab)
        self.forecastTabWindow.addTab(analyticsTab, str(len(self.tabs)))
        forecast = list(data[-1:]) + list(forecast)
        analyticsTab.createForecast(data, forecast)
        self.forecastTabWindow.setCurrentIndex(len(self.tabs) - 1)
    def nextTab(self):
        if len(self.tabs) > 0:
            index = (self.forecastTabWindow.currentIndex() + 1) % len(self.tabs)
            self.forecastTabWindow.setCurrentIndex(index)
    def prevTab(self):
        if len(self.tabs) > 0:
            index = (self.forecastTabWindow.currentIndex() - 1) % len(self.tabs)
            self.forecastTabWindow.setCurrentIndex(index)
    def closeTab(self):
        index = self.forecastTabWindow.currentIndex()
        self.forecastTabWindow.removeTab(index)


class ForecastTab(QTabWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
class APIWindow(QWidget):
    """
    This is the leftmost section of the main window that allows the user to 
    select the data parameters, such as API source, range, and intervals.
    """
    def __init__(self):
        super().__init__()
        self._getSymbolListsAndInfo()
        self.setMaximumWidth(800)
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
        self.rangeEdit.setText("1")
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
            rangeVal = abs(int(range_str))
            if source == "coingecko":
                if 1 <= rangeVal <= 2: index = 0
                elif 2 < rangeVal <= 30: index = 1
                elif rangeVal > 30: index = 2
                else: 
                    index = 0
                intervals = [intervals[index]]
                self.errLabel.setText("Allowed values for CG range: " + get_comma_separated_list(self.api_dict['coingecko'].get_range()))
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
        self.ids = dict(zip(sources_list, [sorted(list(set(api.get_ids()))) for api in list(self.api_dict.values())]))
        self.intervals = dict(zip(sources_list, [format_intervals(api.get_intervals()) for api in list(self.api_dict.values())]))
    def getInterval(self):
        ### This converts the interval string into an integer in minutes
        intervalString = self.intervalComboBox.currentText()
        if len(intervalString) > 7: 
            interval = int(intervalString.split()[0]) * 24 * 60
        else:
            dt = datetime.strptime(intervalString, "%H:%M:%S")
            td = timedelta(hours = dt.hour, minutes = dt.minute, seconds = dt.second)
            interval = int(td.seconds / 60)
        return interval
        #######
    def getSymbol(self) -> str:
        symbolWidget = self.symbolListWidget.currentItem()
        if symbolWidget == None:
            return None
        return symbolWidget.text()
    def getData(self) -> np.ndarray:
        """
        To get the data from the values on the window, the values are first 
        validated, then sent into the desired API for data retrieval.

        :return: 
        """
        ### Getting the source API from the sourceComboBox
        source = self.sourceComboBox.currentText()
        #######
        ### Verifying that a symbol has been selected from the list
        symbol = self.getSymbol()
        if symbol == None:
            self.errLabel.setText("Must select a symbol.")
            return
        #######
        ### Did the user supply a range value?
        rangeVal = self.rangeEdit.text()
        if len(rangeVal) == 0:
            self.errLabel.setText("Range must be at least 1.")
            return
        rangeVal = int(rangeVal)
        #######
        ### Reset the error label
        self.errLabel.setText("")
        #######
        ### Get the inteval in the interval combo box
        interval = self.getInterval()
        #######
        if source == "kraken":
            # UNEXPLAINABLE TYPE ERROR OCCURRING HERE. Clearly passing 4 arguments but it thinks I'm passing 5
            data = self.api_dict[source].get_opening_price(symbol, "USD", rangeVal, interval)
        ### If CoinGecko API is used, the range must be in the array returned by CoinGecko.get_range(), defined in get_data.py
        if source == "coingecko":
            allowed_range = self.api_dict["coingecko"].get_range()
            if rangeVal > 365:
                rangeVal = "max"
            elif rangeVal not in allowed_range:
                rangeVal = allowed_range[np.argmin(np.abs(rangeVal - allowed_range))]
                self.rangeEdit.setText("{}".format(rangeVal))
                self.errLabel.setText("Setting range to the nearest value in {}.".format(allowed_range))
            data = self.api_dict[source].get_opening_price(symbol, "USD", rangeVal)
        #######
        if source == "cmc":
            data = self.api_dict[source].get_opening_price(symbol)[-1*rangeVal:]
        return data

class MLWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.paramEditors = {}
        #self.setMaximumWidth(300)
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
        self.nStepsForward = QLineEdit()
        self.nStepsForward.setValidator(lineEditValidator)
        self.errLabel = QLabel()
        self.forecastButton = QPushButton("New Forecast")
        self.paramEditors["lags"] = self.lagsLineEdit
        self.paramEditors["n_estimators"] = self.nEstimatorsLineEdit
        self.paramEditors["max_depth"] = self.maxDepthLineEdit
        self.paramEditors["max_iter"] = self.maxIterLineEdit
        self.paramEditors["N"] = self.nStepsForward
        self.formLayout.addRow("Regression Model:", self.modelComboBox)
        self.formLayout.addRow("Lags:", self.lagsLineEdit)
        self.formLayout.addRow("Number of Estimators:", self.nEstimatorsLineEdit)
        self.formLayout.addRow("Max Depth:", self.maxDepthLineEdit)
        self.formLayout.addRow("Max Iterations:", self.maxIterLineEdit)
        self.formLayout.addRow("Predict Next N Steps:", self.nStepsForward)
        self.formLayout.addRow("", self.forecastButton)
        self.formLayout.addRow("", self.errLabel)
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
    def getHyperparameters(self) -> dict:
        params = {}
        for param_key, editor in self.paramEditors.items():
            if(editor.isEnabled()):
                param_val = editor.text()
                if param_val == "":
                    self.errLabel.setText("\"{}\" field cannot be empty.".format(param_key))
                    return 
                params[param_key] = int(param_val)
                #print("{}: {}".format(param_key, params[param_key]))
        return params
    def getModel(self):
        return self.modelComboBox.currentText()
    def getPrediction(self, data) -> List[float]:
        model = self.modelComboBox.currentText()
        hyperparameters = self.getHyperparameters()
        if hyperparameters is None:
            return
        if hyperparameters["lags"] > len(data) // 2:
            self.errLabel.setText("Setting lags={}".format(len(data) // 2))
            hyperparameters["lags"] = len(data) // 2
        prediction = predict_next_N_timesteps(data, model, **hyperparameters)
        return prediction

class AnalyticsWindow(QWidget):
    def __init__(self, symbol: str, model: str, interval: int, hyperparameters: dict):
        super().__init__()
        self.symbol = symbol
        self.model = model
        self.interval = interval
        self.hyperparameters = hyperparameters
        self.formLayout = QFormLayout(self)
        self.forecastedPricesListWidget = QListWidget()
        self.forecastedPricesListWidget.setMinimumWidth(300)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.showFullScreen()
        #fullScreenAction = QAction("&Fullscreen", self.graphWidget, shortcut="F", triggered = self.graphWidget.maximize)
        #self.graphWidget.addAction(fullScreenAction)
        #self.graphWidget.setBackground("w")
        self.graphWidget.setMinimumWidth(self.graphWidget.height())
        self.formLayout.addRow("", self.graphWidget)
        self.formLayout.addRow("Forecast (USD):", self.forecastedPricesListWidget)
    def plot(self, historicalY: List[float], forecastedY: List[float]):
        historicalX = [i for i in range(len(historicalY))]
        startForecastX = historicalX[-1]
        forecastedX = [i for i in range(startForecastX, startForecastX + len(forecastedY))]
        hPen = pg.mkPen('#00FFFF', width=3)
        fPen = pg.mkPen('r', width=3)
        self.graphWidget.plot(historicalX, historicalY, pen = hPen, name = "Historical Prices")
        self.graphWidget.plot(forecastedX, forecastedY, pen = fPen, name = "Predicted Prices")
        labelColor = (255, 255, 255)
        self.graphWidget.setLabel("top", "Model: {}; Hyperparameters: {}".format(self.model, str(self.hyperparameters)))
        self.graphWidget.setLabel("left", "{} Price (USD)".format(self.symbol))
        self.graphWidget.setLabel("bottom", "Interval: {} (min)".format(self.interval))
    def createForecast(self, historicalY, forecastedY):
        start = int(time.time())
        self.forecastedPricesListWidget.addItem("Model: {}".format(self.model))
        self.forecastedPricesListWidget.addItem("Hyperparameters: " + str(self.hyperparameters))
        self.forecastedPricesListWidget.addItems(["Time: {}\t Price: {}". \
            format(datetime.fromtimestamp(start + i * self.interval * 60). \
                strftime("%Y-%m-%d %H:%M:%S"), price) for i, price in enumerate(forecastedY)])
        self.plot(historicalY, forecastedY)

class ClassificationWindow(QWidget):
    """
    This is the second primary tab of the window. This implements the functionality
    for 
    """
    def __init__(self, parent = None):
        super().__init__(parent)
        self.gridLayout = QGridLayout(self)
        self.apiWindow = APIWindow()
        self.nnWindow = NNWindow()
        self.gridLayout.addWidget(self.apiWindow, 0, 0)
        self.gridLayout.addWidget(self.nnWindow, 0, 1)

class NNWindow(QWidget):
    """
    This window goes to the right of the API selection window. Users can select 
    various hyperparameters for 
    """
    def __init__(self, parent = None):
        super().__init__(parent)
        self.formLayout = QFormLayout(self)
        self.epochsEdit = QLineEdit()
        self.epochsEdit.setValidator(lineEditValidator)
        self.batchEdit = QLineEdit()
        self.batchEdit.setValidator(lineEditValidator)
        self.lagsEdit = QLineEdit()
        self.lagsEdit.setValidator(lineEditValidator)
        #self.layerEdit = QLineEdit()
        #layerValidator = QRegularExpressionValidator(r"[1-5]")
        self.layerComboBox = QComboBox()
        self.layerComboBox.addItems([str(i) for i in range(1, max_layers + 1)])
        # Update the number of hidden layer widgets depending on the value in 
        self.lossComboBox = QComboBox()
        self.lossComboBox.addItems(["mean_squared_error", "mean_absolute_error", 
                                    "cosine_similarity", "mean_absolute_percentage_error",
                                    "mean_squared_logarithmic_error"])
        self.layerComboBox.currentIndexChanged.connect(self._updateLayerWidgets)
        self.formLayout.addRow("Lags:", self.lagsEdit)
        self.formLayout.addRow("Epochs:", self.epochsEdit)
        self.formLayout.addRow("Batch Size:", self.batchEdit)
        self.formLayout.addRow("Hidden Layers:", self.layerComboBox)
        self.formLayout.addRow("Loss Function:", self.lossComboBox)
        # This adds the dynamic layer parameter tuning for layers 1 through n
        self.createLayerWidgets()
        self._updateLayerWidgets()

    def createLayerWidgets(self):
        self.layerWidgets = []
        for i in range(max_layers):
            widget = QWidget()
            formLayout = QFormLayout(widget)
            self.layerWidgets.append(widget)
            neuronEdit = QLineEdit()
            neuronEdit.setValidator(lineEditValidator)
            activationComboBox = QComboBox()
            activationComboBox.addItems(["relu", "sigmoid", "selu", "elu", 
                                         "tanh", "softplus", "softsign"])
            layerLabel = QLabel("Layer %d" % (i + 1))
            hBox = QHBoxLayout()
            l1Check = QCheckBox("L1")
            l2Check = QCheckBox("L2")
            dropoutCheck = QCheckBox("Dropout")
            hBox.addWidget(l1Check)
            hBox.addWidget(l2Check)
            hBox.addWidget(dropoutCheck)
            formLayout.addRow("", layerLabel)
            formLayout.addRow("Units/Neurons:", neuronEdit)
            formLayout.addRow("Activation Function:", activationComboBox)
            formLayout.addRow("Regularization:", hBox)
            self.formLayout.addRow("", widget)
        widget = QWidget()
        formLayout = QFormLayout(widget)
        self.layerWidgets.append(widget)
        activationComboBox = QComboBox()
        activationComboBox.addItems(["sigmoid"])
        formLayout.addRow(QLabel("Output Layer"))
        formLayout.addRow(activationComboBox)
        self.trainButton = QPushButton("Train")
        self.formLayout.addRow(widget)
        self.formLayout.addRow(self.trainButton)

    def _updateLayerWidgets(self):
        layers = int(self.layerComboBox.currentText())
        for i in range(max_layers):
            self.layerWidgets[i].setVisible(i < layers)

def start_gui():
    """
    Starts up a gui session
    """
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    start_gui()