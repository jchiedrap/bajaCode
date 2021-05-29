import pandas as pd
import gmplot, os
from pandas.core.frame import DataFrame

def turnToDf(filePath: str):
    return pd.read_csv(filePath)

def splitCsvInDfIfDuplicateHeaders(filePath: str): #Make this create separate data frames instead of csv's
    df = turnToDf(filePath)
    dfList = []
    #preLine is last line to iterate the csv from
    #curLine is current line to iterate the csv to
    #csvNumber is the current number of the csv generated, starting with 1
    prevLine, curLine, csvNumber = 0, 0, 0
    for index, row in df.iterrows():
        curLine += 1  
        if df.loc[index,"RPM"] == "RPM":
            currDf = df.iloc[prevLine:curLine-1]#Skips over line where the repeat header was recognized
            dfList.append(currDf)
            prevLine = curLine
    lastDf = df.iloc[prevLine:]
    dfList.append(lastDf)
    return dfList

def createDirectory(folderName: str, childFolders: list): #Creates working directory within the user's home directory on Windows
    BAJAFolder = os.path.join(os.environ['USERPROFILE'], folderName)
    if not os.path.exists(BAJAFolder):
        for folder in childFolders:
            os.makedirs(os.path.join(BAJAFolder, folder))

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

def createHTMLFile(mapPlot: gmplot.GoogleMapPlotter,folderName: str, outputName: str):
    mapPlot.draw(os.path.join(os.environ['USERPROFILE'], folderName, 'html', outputName))
    
def openHTMLFile(folderName: str, outputName: str):
    os.system('"' + os.path.join(folderName, 'html', outputName) + '"')


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
    
    
def turnToExcel(df: DataFrame, folderName: str, outName: str, fileNum: int = 1):
    if fileNum != 1:
        df.to_excel(os.path.join(os.environ['USERPROFILE'], folderName, 'xlsx', outName + '_' + str(fileNum) + '.xlsx'), 
                index=False)
    else:
        df.to_excel(os.path.join(os.environ['USERPROFILE'], folderName, 'xlsx', outName + '.xlsx'), 
                index=False)

def turnToCSV(df: DataFrame, folderName: str, outName: str, fileNum: int = 1):
    if fileNum != 1:
        df.to_csv(os.path.join(os.environ['USERPROFILE'], folderName, 'csv', outName + '_' + str(fileNum) + '.csv'), 
                index=False)
    else:
        df.to_csv(os.path.join(os.environ['USERPROFILE'], folderName, 'csv', outName + '.csv'), 
                index=False)

def processData(path: str, 
                outName: str, 
                variableToBeMeasured: str, 
                minVal: float, maxVal: float, 
                folderName: str = 'BAJAPlots', 
                childFolders: list = ['html', 'xlsx', 'csv']
               ):
    dfList = splitCsvInDfIfDuplicateHeaders(path)
    createDirectory(folderName, childFolders)
    
    fileNum = 0
    for dataFrame in dfList:
        fileNum += 1
        mapDf(dataFrame, folderName, outName, variableToBeMeasured, minVal, maxVal, fileNum)
        turnToExcel(dataFrame, folderName, outName, fileNum)
        turnToCSV(dataFrame, folderName, outName, fileNum)
