import matplotlib.pyplot as plt
import pandas as pd
from datetime import time
#Finished Jan 6th 2020
def plotData(path, quantity):

    df = pd.read_csv(path)

    timeArray = [time( int(timestring[7:9]), int(timestring[9:11]), second = int(timestring[11:13])) for timestring in [str(df.loc[index, 'DDMMYYYYHHMMSS']) for index, row in df.iterrows()]]
   
    timeArray = pd.to_datetime(timeArray, format="%H:%M:%S")#Converting into pandas time format (with standard year, month, day)
    plt.xticks(rotation=30)
    
    plt.plot(timeArray, df[quantity])
    plt.title(f'{quantity} vs Time')
    plt.xlabel('Time')
    plt.ylabel(f'{quantity}')
    plt.show()
    