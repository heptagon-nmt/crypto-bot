from tkinter import W
from get_data import *
import sys
from PySide6 import Qt, QtCore
from PySide6.QtGui import QAction, QKeySequence, QPalette
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
    QFormLayout, QGridLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QToolBar, QWidget)



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
        exitAction = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        self.centralWidget = CentralWidget()
        self.setCentralWidget(self.centralWidget)

    def load(self):
        QMessageBox.warning(self, "AxViewer", f"Unable to load the veendow.")

class CentralWidget(QWidget):
    """
    This is the widget to contain the APIWindow, MLWindow, as well as 
    AnalyticsWindow and GraphsWindow.

    Attributes:

    """
    def __init__(self):
        super().__init__()
        self.gridLayout = QGridLayout(self)

        apiWindow = APIWindow()
        
        self.gridLayout.addWidget(apiWindow, 0, 0)

class APIWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._getSymbolListsAndInfo()

        formLayout = QFormLayout(self)
        self.sourceComboBox = QComboBox()
        self.sourceComboBox.addItems(sources_list)
        self.sourceComboBox.currentIndexChanged.connect(self._sourceChangeMethod)
        self.symbolFilter = QLineEdit()
        self.symbolFilter.setPlaceholderText("ID (e.g. ethereum)")
        self.symbolFilter.textChanged.connect(self.populate_symbols)
        self.symbolListWidget = QListWidget()
        self.symbolListWidget.itemSelectionChanged.connect(self.updateSelected)
        self.selectedSymbol = QLabel()
        self.intervalComboBox = QComboBox()
        self.rangeEdit = QLineEdit()
        self.rangeEdit.setPlaceholderText("Number of days behind the current to collect data.")

        formLayout.addRow("API Source:", self.sourceComboBox)
        formLayout.addRow("Symbol:", self.symbolFilter)
        formLayout.addRow("", self.symbolListWidget)
        formLayout.addRow("Selected Symbol:", self.selectedSymbol)
        formLayout.addRow("Range:", self.rangeEdit)
        self.populate_symbols()
    def populate_symbols(self):
        source = self.sourceComboBox.currentText()
        search = self.symbolFilter.displayText()
        displayedSymbols = [symbol for symbol in self.ids[source] 
                                if search.upper() in symbol.upper()]
        self.symbolListWidget.clear()
        self.symbolListWidget.addItems(displayedSymbols)
    def setIntervals(self):
        """
        """
        source = self.sourceComboBox.currentText()
        if source == "coingecko":
            self.intervalComboBox.setEditable(False)
        if source == "kraken":
            self.intervalComboBox.setEditable(True)
        pass
    def updateSelected(self):
        selectedItem = self.symbolListWidget.currentItem()
        if selectedItem is not None:
            self.selectedSymbol.setText(selectedItem.text())
    def _sourceChangeMethod(self):
        self.populate_symbols()
        self.setIntervals()
    def _getSymbolListsAndInfo(self):
        coingecko = CoinGecko()
        kraken = Kraken()
        cmc = CMC()
        self.ids = dict(zip(sources_list, [coingecko.get_ids(), kraken.get_ids(), cmc.get_ids()]))
        self.intervals = dict(zip(sources_list, [coingecko.get_intervals(), kraken.get_intervals(), cmc.get_intervals()]))


class MLWindow(QWidget):
    def __init__(self):
        super().__init__()

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()

class GraphsWindow(QWidget):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
    mainWin.show()
    sys.exit(app.exec())
