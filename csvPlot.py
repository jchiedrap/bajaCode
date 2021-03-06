import matplotlib.pyplot as plt
import pandas as pd
from datetime import time
def plotData(path: str, quantity: str):

    df = pd.read_csv(path) #Read the csv
    
    timeArray = [time( hour = int(timestring[3]), minute = int(timestring[4]), second = int(timestring[5]) ) 
                 for timestring in [str(df.loc[index, 'DD-MM-YYYY-HH-MM-SS']).split('-') for index, row in df.iterrows()] ]
    
    timeArray = pd.to_datetime(timeArray, format="%H:%M:%S")#Converting into pandas time format (with standard year, month, day)
    plt.xticks(rotation=30) #Rotate the x-axis labels 30 degrees so they don't overlap
    
    plt.plot(timeArray, df[quantity]) #Plot the graph
    plt.title(f'{quantity} vs Time') #Give the title
    plt.xlabel('Time')
    plt.ylabel(f'{quantity}')
    plt.show()
