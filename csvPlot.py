import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
#Old code from Jan 6th with the one-liner
def plotData(path, quantity):

    df = pd.read_csv(path)

    time = [datetime(int(timestring[3:7]), int(timestring[1:3]), int(timestring[0:1]), int(timestring[7:9]), int(timestring[9:11]), second = int(timestring[11:13])) for timestring in [str(df.loc[index, 'DDMMYYYYHHMMSS']) for index, row in df.iterrows()]]
        
    plt.plot(time, df[quantity])
    plt.title(f'{quantity} vs Time')
    plt.xlabel('Time')
    plt.ylabel(f'{quantity}')
    plt.show()
