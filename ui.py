
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(586, 436)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(130, 0, 321, 71))
        font = QtGui.QFont()
        font.setFamily("MS UI Gothic")
        font.setPointSize(24)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.routeButton = QtWidgets.QPushButton(self.centralwidget)
        self.routeButton.setGeometry(QtCore.QRect(10, 230, 131, 31))
        self.routeButton.setObjectName("routeButton")
        self.quantityButton = QtWidgets.QPushButton(self.centralwidget)
        self.quantityButton.setGeometry(QtCore.QRect(10, 180, 141, 41))
        self.quantityButton.setObjectName("quantityButton")
        self.combo_Y = QtWidgets.QComboBox(self.centralwidget)
        self.combo_Y.setGeometry(QtCore.QRect(10, 100, 73, 22))
        self.combo_Y.setObjectName("combo_Y")
        self.combo_Y.addItem("")
        self.combo_Y.addItem("")
        self.combo_Y.addItem("")
        self.combo_Y.addItem("")
        self.combo_Y.addItem("")
        self.combo_Y.addItem("")
        self.y_axis_label = QtWidgets.QLabel(self.centralwidget)
        self.y_axis_label.setGeometry(QtCore.QRect(30, 70, 55, 16))
        self.y_axis_label.setObjectName("y_axis_label")
        self.x_axis_label = QtWidgets.QLabel(self.centralwidget)
        self.x_axis_label.setGeometry(QtCore.QRect(90, 70, 55, 16))
        self.x_axis_label.setObjectName("x_axis_label")
        self.combo_X = QtWidgets.QComboBox(self.centralwidget)
        self.combo_X.setGeometry(QtCore.QRect(90, 100, 73, 22))
        self.combo_X.setObjectName("combo_X")
        self.combo_X.addItem("")
        self.combo_X.addItem("")
        self.combo_X.addItem("")
        self.combo_X.addItem("")
        self.combo_X.addItem("")
        self.combo_X.addItem("")
        self.excelButton = QtWidgets.QPushButton(self.centralwidget)
        self.excelButton.setGeometry(QtCore.QRect(10, 140, 141, 31))
        self.excelButton.setObjectName("excelButton")
        self.plotMapAreaTab = QtWidgets.QTabWidget(self.centralwidget)
        self.plotMapAreaTab.setGeometry(QtCore.QRect(210, 60, 361, 321))
        self.plotMapAreaTab.setObjectName("plotMapAreaTab")
        self.routeTab = QtWidgets.QWidget()
        self.routeTab.setObjectName("routeTab")
        self.plotMapAreaTab.addTab(self.routeTab, "")
        self.graphTab = QtWidgets.QWidget()
        self.graphTab.setObjectName("graphTab")
        self.plotMapAreaTab.addTab(self.graphTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 586, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionImport_csv_file = QtWidgets.QAction(MainWindow)
        self.actionImport_csv_file.setObjectName("actionImport_csv_file")
        self.actionExport_Excel_File = QtWidgets.QAction(MainWindow)
        self.actionExport_Excel_File.setObjectName("actionExport_Excel_File")
        self.actionSplit_CSV_File = QtWidgets.QAction(MainWindow)
        self.actionSplit_CSV_File.setObjectName("actionSplit_CSV_File")
        self.menuFile.addAction(self.actionImport_csv_file)
        self.menuFile.addAction(self.actionExport_Excel_File)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.plotMapAreaTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titleLabel.setText(_translate("MainWindow", "BAJA Run Analysis"))
        self.routeButton.setText(_translate("MainWindow", "Plot Route"))
        self.quantityButton.setText(_translate("MainWindow", "Plot Quantity vs. Time"))
        self.combo_Y.setItemText(0, _translate("MainWindow", "Time"))
        self.combo_Y.setItemText(1, _translate("MainWindow", "RPM"))
        self.combo_Y.setItemText(2, _translate("MainWindow", "Gas"))
        self.combo_Y.setItemText(3, _translate("MainWindow", "Speed"))
        self.combo_Y.setItemText(4, _translate("MainWindow", "Latitude"))
        self.combo_Y.setItemText(5, _translate("MainWindow", "Longitude"))
        self.y_axis_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Y-Axis</p></body></html>"))
        self.x_axis_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">X-Axis</p></body></html>"))
        self.combo_X.setItemText(0, _translate("MainWindow", "Time"))
        self.combo_X.setItemText(1, _translate("MainWindow", "RPM"))
        self.combo_X.setItemText(2, _translate("MainWindow", "Gas"))
        self.combo_X.setItemText(3, _translate("MainWindow", "Speed"))
        self.combo_X.setItemText(4, _translate("MainWindow", "Latitude"))
        self.combo_X.setItemText(5, _translate("MainWindow", "Longitude"))
        self.excelButton.setText(_translate("MainWindow", "Create Excel File"))
        self.plotMapAreaTab.setTabText(self.plotMapAreaTab.indexOf(self.routeTab), _translate("MainWindow", "Route"))
        self.plotMapAreaTab.setTabText(self.plotMapAreaTab.indexOf(self.graphTab), _translate("MainWindow", "Graph"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionImport_csv_file.setText(_translate("MainWindow", "Import CSV File"))
        self.actionExport_Excel_File.setText(_translate("MainWindow", "Export Excel File"))
        self.actionSplit_CSV_File.setText(_translate("MainWindow", "Split CSV File"))


#Logic Class
import pandas as pd
import gmplot, os
from pandas.core.frame import DataFrame

from PyQt5.QtWidgets import QFileDialog
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        dataframes = []
        self.setupUi(self)
        self.setWindowTitle("BAJA Run Data Analysis")
        self.createDirectory('BAJAPlots', ['html', 'xlsx', 'csv'])
        self.routeButton.clicked.connect(self.plotRoute)
        self.actionImport_csv_file.triggered.connect(self.importCSV)
    
    def createDirectory(self, folderName: str, childFolders: list): #Creates working directory within the user's home directory on Windows
        BAJAFolder = os.path.join(os.environ['USERPROFILE'], folderName)
        if not os.path.exists(BAJAFolder):
            for folder in childFolders:
                os.makedirs(os.path.join(BAJAFolder, folder))
                
    def turnToDf(self, filePath: str):
        return pd.read_csv(filePath)
    
    def splitCsvInDfIfDuplicateHeaders(self, filePath: str): #Make this create separate data frames instead of csv's
        df = self.turnToDf(filePath)
        dfList = []
        #preLine is last line to iterate the csv from
        #curLine is current line to iterate the csv to
        prevLine, curLine = 0, 0
        for index, row in df.iterrows():
            curLine += 1  
            if df.loc[index,"RPM"] == "RPM":
                currDf = df.iloc[prevLine:curLine-1]#Skips over line where the repeat header was recognized
                dfList.append(currDf)
                prevLine = curLine
        lastDf = df.iloc[prevLine:]
        dfList.append(lastDf)
        return dfList
                
    def importCSV(self):
        file, _filter = QFileDialog.getOpenFileName(self,
                                           'Importing csv file', 
                                           '',
                                           "All Files (*);;Text Files (*.txt);;Excel Files (*.xlsx);;csv Files (*.csv)", 
                                           options=QFileDialog.Options())
        self.dataframes = self.splitCsvInDfIfDuplicateHeaders(file)
        
    def plotRoute(self):
        print('assume the route is showing up properly lol')
        
    def colorPick (val: float, minVal: float, maxVal: float):
        if val >= maxVal or val <= minVal: # Bounds are exclusive
            return '#FFFFFF' # out of bounds, return white 
        
        delta = (maxVal - minVal)
        intervalSize = delta / 4 # 4 steps, 0000ff -> 00ffff, 00ffff -> 00ff00, etc...
        interval = (val-minVal) // intervalSize # gives us which of the intervals we are at
        gain = ((val-minVal) % intervalSize) / intervalSize # gives us how far we are past the interval step as a decimal representation of a percentage
        
        #Colours in Order from lowest to highest: blue, cyan , green, yellow, red
        if interval == 0:
            red, green, blue = 0, int(255*gain), 255
        elif interval == 1:
            red, green, blue = 0, 255, int(255*(1-gain))
        elif interval == 2:
            red, green, blue = int(255*gain), 255, 0
        elif interval == 3:
            red, green, blue = 255, int(255*(1-gain)), 0
       
        return '#{:02x}{:02x}{:02x}'.format(red, green, blue)

    def mapDf(df: DataFrame, 
          folderName: str, 
          outName: str, 
          variableToBeMeasured: str, 
          minVal: float, 
          maxVal: float,
          fileNum: int = 1 
         ):
        if fileNum != 1:
            outputName = '{}_{}.html'.format(outName, fileNum)
        else:
            outputName = '{}.html'.format(outName)
        
        minLat = min([float(x) for x in df['Latitude'] if float(x) != 0.0])
        minLon = min([float(x) for x in df['Longitude'] if float(x) != 0.0])
        maxLat = max([float(x) for x in df['Latitude'] if float(x) != 0.0])
        maxLon = max([float(x) for x in df['Longitude'] if float(x) != 0.0])
        
        #Approximate location of the course
        mapPlot = gmplot.GoogleMapPlotter((minLat + (maxLat - minLat)/2), (minLon + (maxLon - minLon)/2), 18)
        for index, row in df.iterrows():
            if (float(df.loc[index,'Latitude']) != 0.0 and float(df.loc[index, 'Longitude']) != 0.0): 
                mapPlot.plot(df.loc[index:index+1, 'Latitude'].astype(float), df.loc[index:index+1, 'Longitude'].astype(float), color = colorPick(float(df.loc[index,variableToBeMeasured]), minVal, maxVal), edge_width=7)
        
        createHTMLFile(mapPlot, folderName, outputName)
        openHTMLFile(folderName, outputName)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
