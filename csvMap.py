import pandas as pd
import numpy
import gmplot
import os

from pandas.core.frame import DataFrame
#Finished Jan 4th 2020
def turnToDf(filePath: str):
    return pd.read_csv(filePath)

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

def mapDf(df: DataFrame, outName: str, variableToBeMeasured: str, minVal: float, maxVal: float):
    outputName = '{}.html'.format(outName)
    minLat, minLon, maxLat, maxLon = min([x for x in df['Latitude'] if x != 0.0]), min([x for x in df['Longitude'] if x != 0.0]), max([x for x in df['Latitude'] if x != 0.0]), max([x for x in df['Longitude'] if x != 0.0])
    #Approximate location of the course
    mapPlot = gmplot.GoogleMapPlotter((minLat + (maxLat - minLat)/2), (minLon + (maxLon - minLon)/2), 18)
    for index, row in df.iterrows():
        if (df.loc[index,"Latitude"] != 0.0 and df.loc[index, "Longitude"] != 0.0) : mapPlot.plot(df.loc[index:index+1, 'Latitude'], df.loc[index:index+1, 'Longitude'], color = colorPick(df.loc[index,variableToBeMeasured], minVal, maxVal), edge_width=7)
    mapPlot.draw(outputName)
    os.system(outputName)
    
def turnToExcel(df: DataFrame, outName: str):
    df.to_excel('{}.xlsx'.format(outName))

def processData(inName: str, outName: str, variableToBeMeasured: str, minVal: float, maxVal: float):
    df = turnToDf(inName)
    mapDf(df, outName, variableToBeMeasured, minVal, maxVal)
    turnToExcel(df, outName)
