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

# Read CSV
df = pd.read_csv('./potato_rates.csv')
# Change values to float
df['Modal Price'] = df['Modal Price'].astype('float')
df['Max Price'] = df['Max Price'].astype('float')
df['Min Price'] = df['Min Price'].astype('float')
df['Price Date'] = df['Price Date'].astype('string')

# Select only 2016 data
# df = df[df['Price Date'].str.contains('-16')]

# Convert Rs/kg
df['Modal Price'] = np.divide(df['Modal Price'], 100)
df['Max Price'] = np.divide(df['Max Price'], 100)
df['Min Price'] = np.divide(df['Min Price'], 100)
df['Price Date'] = pd.to_datetime(df['Price Date'])

for r in df['Price Date']:
    arr.append(r.year)
for r in df['Price Date']:
    arr.append(r.month)
for r in df['Price Date']:
    arr.append(r.year)
for r in df['Price Date']:
    arr.append(r.year)
df['Year'] = pd.Series(arr)

print df['Year']
exit()
df = DataFrame({'Modal Price':df.groupby('Price Date')['Modal Price'].mean()}).reset_index()
#
# a = df['Modal Price'].copy().sort(inplace=False)
# hmean = np.mean(a)
# hstd = np.std(a)
# pdf = stats.norm.pdf(a, hmean, hstd)
# plt.plot(a, pdf)
# plt.show()
# exit()

# X-Axis manipulation
df['Year'] = pd.DatetimeIndex(df['Price Date']).year
df['Month'] = pd.DatetimeIndex(df['Price Date']).month


# print 'Average Rate',np.average(df['Modal Price'])
# print 'Max Rate',df['Modal Price'].max()
# print 'Min Rate',df['Modal Price'].min()
fig = plt.figure()
fig.suptitle('Tomato - 2010-16'+'\n\nMax Rate - '+str(df['Modal Price'].max())+'\n\nMin Rate - '+str(df['Modal Price'].min())+'\n\nAverage Rate - '+str(round(np.average(df['Modal Price']),2)), fontsize=14)
plt.xlabel('', fontsize=12)
plt.ylabel('Rs/Kg', fontsize=12)
# plt.plot_date(df['Price Date'], df['Modal Price'])
# count = 0
# for a in df['Year']:
#     if(a == 6):
#         print df['Price Date'][count]
#         count += 1
#
# print count
# plt.scatter(df['Year'], df['Modal Price'])
plt.plot_date(df['Price Date'], df['Modal Price'])
plt.show()

# print df['Price Date']
