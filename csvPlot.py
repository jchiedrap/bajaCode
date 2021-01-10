import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
#Old Code from Jan 6th
def plotData(path, quantity):

    df = pd.read_csv(path)
    time = []

    for index, row in df.iterrows():
        timestring = str(df.loc[index,'DDMMYYYYHHMMSS'])
        year = int(timestring[3:7]) ###
        month = int(timestring[1:3]) ###
        day = int(timestring[0:1]) ###
        hour = int(timestring[7:9])
        minute = int(timestring[9:11])
        second = int(timestring[11:13])

        time.append(datetime(year, month, day, hour, minute, second))
        
    plt.plot(time, df[quantity])
    plt.title(f'{quantity} vs Time')
    plt.xlabel('Time')
    plt.ylabel(f'{quantity}')
    plt.show()
