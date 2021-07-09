import pandas as pd
import gmplot, os
import sys
from pandas.core.frame import DataFrame
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QFileDialog, QTextBrowser
from BAJA_Data_Analysis_UI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    folderName = 'BAJAPlots'
    childFolders = ['html', 'xlsx', 'csv']
    apikey = 'AIzaSyC26WMAPVQUgCheJftUx_wxWeQ5-UaUx3A'
    previousImport = ''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.dataframes = []
        self.dataframeNum = 0
        self.dataframeCount = 0
        self.currentFileName = ''
        self.setWindowTitle("BAJA Run Data Analysis")
        self.createDirectory(self.folderName, self.childFolders)
        self.routeButton.clicked.connect(self.plotRoute)
        self.leftDataframeSelector.clicked.connect(self.leftSelect)
        self.rightDataframeSelector.clicked.connect(self.rightSelect)
        self.actionImport_csv_file.triggered.connect(self.importCSV)
        self.actionExport_Excel_File.triggered.connect(self.exportExcel)
        self.actionExport_html_File.triggered.connect(self.exportHTML)
        
    def leftSelect(self):
        if self.dataframeNum > 0:
            self.dataframeNum -= 1
            self.dataframeLabel.setText('Dataframe {}'.format(self.dataframeNum))
        
    def rightSelect(self):
        if self.dataframeNum < len(self.dataframes) - 1:
            self.dataframeNum += 1
            self.dataframeLabel.setText('Dataframe {}'.format(self.dataframeNum))
        
    def importCSV(self):
        try:
            fileName, _filter = QFileDialog.getOpenFileName(self,
                                               'Import csv file', 
                                               self.previousImport,
                                               "All Files (*);;Text Files (*.txt);;Excel Files (*.xlsx);;csv Files (*.csv)", 
                                               options=QFileDialog.Options())
            self.dataframes = self.splitCsvInDfIfDuplicateHeaders(fileName)
            self.currentFileName = os.path.basename(fileName)
            self.fileLabel.setText('FileName: \"{}\"'.format(self.currentFileName))
        except FileNotFoundError:
            self.errorLabel.setText("Please Select a Dataframe")
        except pd.errors.ParserError:
            self.errorLabel.setText("Please Select a Dataframe")
            
        
    def exportExcel(self):
        name, _filter = QFileDialog.getSaveFileName(self,
                                           'Export excel file', 
                                           self.currentFileName,
                                           "Excel Files (*.xlsx)", 
                                           options=QFileDialog.Options())
        try:
            self.dataframes[self.dataframeNum].to_excel(os.path.join(os.environ['USERPROFILE'], self.folderName, 'xlsx', name + '.xlsx'), 
                index=False)
            self.errorLabel.setText("")
        except ValueError: #Usually occurs due to user saving with no name
            pass
        except IndexError:
            self.errorLabel.setText("Please Select a Dataframe")
        
    def exportHTML(self):
        name, _filter = QFileDialog.getSaveFileName(self,
                                           'Export html file', 
                                           self.currentFileName,
                                           "html Files (*.html)", 
                                           options=QFileDialog.Options())
        try:
            self.mapDf(self.dataframes[self.dataframeNum], 
                       self.folderName, 
                       name, 
                       self.quantityComboBox.currentText(), 
                       float(self.minValLineEdit.text()), 
                       float(self.maxValLineEdit.text()),
                       self.dataframeNum
                       )
            self.errorLabel.setText("")
        except ValueError:
            #Usually occurs if user does not enter proper min/max values
            self.errorLabel.setText("Please Enter Valid Bounds")
        except IndexError:
            self.errorLabel.setText("Please Select a Dataframe")
        
        
    def plotRoute(self):
        try: 
            self.mapDf(self.dataframes[self.dataframeNum], 
                       self.folderName, 
                       'tmp', 
                       self.quantityComboBox.currentText(), 
                       float(self.minValLineEdit.text()), 
                       float(self.maxValLineEdit.text()),
                       self.dataframeNum
                       )
            self.errorLabel.setText("")
            self.webView = QtWebEngineWidgets.QWebEngineView()
            self.loadPage()
            self.webEngineVBox.addWidget(self.webView)
        except IndexError:
            self.errorLabel.setText("Please Select a Dataframe")
        except ValueError: 
            self.errorLabel.setText("Please Enter Valid Bounds")

    
    def loadPage(self):
        #map.html works for some reason
        with open("C:/Users/Tahmeed/BAJAPlots/html/tmp.html", 'r') as f:
            html = f.read()
            with open("C:/Users/Tahmeed/BAJA UI Test Files/test.txt", 'w+') as file:
                file.write(html)
                self.webView.setHtml(html)
            
            f.close()

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
        prevLine = 0#last line to iterate the csv from
        curLine = 0#current line to iterate the csv to
        for index, row in df.iterrows():
            curLine += 1  
            if df.loc[index,"RPM"] == "RPM":
                currDf = df.iloc[prevLine:curLine-1]#Skips over line where the repeat header was recognized
                dfList.append(currDf)
                prevLine = curLine
        lastDf = df.iloc[prevLine:]
        dfList.append(lastDf)
        self.dataframeCount = len(dfList)
        return dfList
        
    def createHTMLFile(self, mapPlot: gmplot.GoogleMapPlotter,folderName: str, outputName: str):
        mapPlot.draw(os.path.join(os.environ['USERPROFILE'], folderName, 'html', outputName))
        
    def mapDf(self,
          df: DataFrame, 
          folderName: str, 
          outName: str, 
          variableToBeMeasured: str, 
          minVal: float, 
          maxVal: float,
          fileNum: int = 0 
         ):
        outputName = '{}.html'.format(outName)
        
        minLat = min([float(x) for x in df['Latitude'] if float(x) != 0.0])
        minLon = min([float(x) for x in df['Longitude'] if float(x) != 0.0])
        maxLat = max([float(x) for x in df['Latitude'] if float(x) != 0.0])
        maxLon = max([float(x) for x in df['Longitude'] if float(x) != 0.0])
        
        #Approximate location of the course
        mapPlot = gmplot.GoogleMapPlotter((minLat + (maxLat - minLat)/2), 
                                          (minLon + (maxLon - minLon)/2), 
                                          18, 
                                          apikey = self.apikey,
                                          map_type='hybrid')
        pathList = []
        colorList = []
        for index, row in df.iterrows():
            if (float(df.loc[index,'Latitude']) != 0.0 and float(df.loc[index, 'Longitude']) != 0.0):
                mapPlot.plot(df.loc[index:index+1, 'Latitude'].astype(float), df.loc[index:index+1, 'Longitude'].astype(float), color = self.colorPick(float(df.loc[index,variableToBeMeasured]), minVal, maxVal), edge_width=7)
                
                #pathList.append( (float(df.loc[index,'Latitude']), float(df.loc[index, 'Longitude'])) )
                #colorList.append( self.colorPick(float(df.loc[index,variableToBeMeasured]), minVal, maxVal) )
        
        #Without the asterisk, the coordinates would be passed as a single argument instead of being unpacked as two
        #With asterisk, you get two tuples, one with all the longs and one with all the lats
        a = str((color) for color in colorList)
        
        """
        mapPlot.heatmap(*path, 
                        opacity = 0.5, 
                        radius=10, 
                        #figure out the weights
                        gradient=[(0, 0, 255, 0), (0, 255, 0, 0.5), (255, 0, 0, 1)] 
                        )
"""
        self.createHTMLFile(mapPlot, folderName, outputName)
        
    #Temporary Function
    def openHTMLPlot(self, outName: str, fileNum: int = 0):
        outputName = '{}.html'.format(outName)
        os.system(os.path.join(os.environ['USERPROFILE'], self.folderName, 'html', outputName))
        
        
    def colorPick (self, val: float, minVal: float, maxVal: float):
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
    
    def closeEvent(self, event):
        for subfolder in self.childFolders:
            tmp_file = os.path.join(os.environ['USERPROFILE'], self.folderName, subfolder, 'tmp.{}'.format(subfolder))
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
