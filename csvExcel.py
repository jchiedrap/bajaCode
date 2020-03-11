import gmplot
import pandas
import os

def turnToDf(filePath):
    return pandas.read_csv(filePath)

def mapDf(df, outName):
    outputName = '{}.html'.format(outName)
    minLat, minLon, maxLat, maxLon = min(df['Latitude']), min(df['Longitude']), max(df['Latitude']), max(df['Longitude'])
    mapPlot = gmplot.GoogleMapPlotter((minLat + (maxLat - minLat)/2), (minLon + (maxLon - minLon)/2), 10)
    mapPlot.plot(df['Latitude'], df['Longitude'], 'red', edge_width=7)
    mapPlot.draw(outputName)
    os.system(outputName)

def turnToExcel(df, outName):
    df.to_excel('{}.xlsx'.format(outName))

def processData(inName, outName):
    df = turnToDf(inName)
    mapDf(df, outName)
    turnToExcel(df, outName)