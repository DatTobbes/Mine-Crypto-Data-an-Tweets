from pandas import read_csv
from pandas import datetime
import matplotlib.pyplot as plt
import numpy as np
import talib



# date-time parsing function for loading the dataset
def parser(x):
    #return datetime.strptime('190' + x, '%Y-%m')
    return datetime.strptime( x, '%Y-%m-%d %H:%M:%S')


series = read_csv('BTC.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
from  Database.Database import DatabaseConnector

values=np.asarray(series.values)

close = np.random.random(100)
output = talib.SMA(values)
print(output)

plt.plot(output)
plt.show()