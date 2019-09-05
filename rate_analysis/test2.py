import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import re
import scipy.stats as stats

arr = []
y_arr = []

# Read CSV
df = pd.read_csv('./potato_rates.csv')
# Change values to float
df['Modal Price'] = df['Modal Price'].astype('float')
df['Max Price'] = df['Max Price'].astype('float')
df['Min Price'] = df['Min Price'].astype('float')
df['Price Date'] = df['Price Date'].astype('string')

# Select only 2016 data
# df = df[df['Price Date'].str.contains('-16')]


def it(a, b):
    x = (b-1)*7
    x = 1 if(x==0) else x
    return str(a)+"-"+str(x).zfill(3)


# Convert Rs/kg
df['Modal Price'] = np.divide(df['Modal Price'], 100)
df['Max Price'] = np.divide(df['Max Price'], 100)
df['Min Price'] = np.divide(df['Min Price'], 100)
df['Price Date'] = pd.to_datetime(df['Price Date'])


times = pd.DatetimeIndex(df['Price Date'])
df = DataFrame({"Modal Price": df.groupby([times.year])['Modal Price'].mean()}).reset_index()
# print df
# exit()
# df['Date'] = pd.Series(pd.to_datetime(map(it, df['index']), format='%Y-%j'))


fig = plt.figure()
fig.suptitle('Potato', fontsize=14)
plt.scatter(df['index'], df['Modal Price'])
# plt.plot_date(df['index'], df['Modal Price'])
plt.show()

# print df['Price Date']
