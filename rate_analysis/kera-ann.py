import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
import re
import scipy.stats as stats

day = []
week = []
month = []
year = []

# Read CSV
df = pd.read_csv('./potato_rates.csv')


# Filter by market
df = df[df['Market Name'].isin(['Azadpur'])]


# Change values to float
df['Modal Price'] = df['Modal Price'].astype('int')
df['Max Price'] = df['Max Price'].astype('int')
df['Min Price'] = df['Min Price'].astype('int')
df['Price Date'] = df['Price Date'].astype('string')


# Convert Rs/kg
# df['Modal Price'] = np.round(np.divide(df['Modal Price'], 100), decimals=0)
# df['Max Price'] = np.round(np.divide(df['Max Price'], 100), decimals=0)
# df['Min Price'] = np.round(np.divide(df['Min Price'], 100), decimals=0)
df['Price Date'] = pd.to_datetime(df['Price Date'])


# Remove Outliers
# mean = np.mean(df['Modal Price'])
# std = np.std(df['Modal Price'])
# df = df[abs(df['Modal Price'] - mean) <= 5*np.std(df['Modal Price'])]
# print df
# exit()


times = pd.DatetimeIndex(df['Price Date'])
df['Year'] = times.year
df['Day'] = times.dayofyear
df['Month'] = times.month
df['Week'] = times.weekofyear

del df['State Name']
del df['Market Name']
del df['Group']
del df['Variety']
del df['Grade']
del df['Price Date']
del df['Max Price']
del df['Min Price']

# print df.head()

y = df['Modal Price'].as_matrix()[:1500]
y_test = df['Modal Price'].as_matrix()[1500:]
del df['Modal Price']
X = df.as_matrix()[:1500]
X_test = df.as_matrix()[1500:]
# df_year = DataFrame({"Modal Price": df.groupby(times.year)['Modal Price'].mean()}).reset_index()
# df_month = DataFrame({"Modal Price": df.groupby(times.month)['Modal Price'].mean()}).reset_index()
# df_week = DataFrame({"Modal Price": df.groupby(times.weekofyear)['Modal Price'].mean()}).reset_index()
# df_day = DataFrame({"Modal Price": df.groupby(times.dayofyear)['Modal Price'].mean()}).reset_index()

X = np.array(X)
y = np.array(y)
X_test = np.array(X_test)
y_test = np.array(y_test)

trainX = numpy.reshape(X, (X.shape[0], 1, X.shape[1]))
testX = numpy.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

#
scaler = MinMaxScaler(feature_range=(0, 1))
# dataset = scaler.fit_transform(dataset)

look_back = 1
model = Sequential()
model.add(LSTM(3, input_dim=look_back))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X, y, nb_epoch=100, batch_size=1, verbose=2)


# Estimate model performance
trainScore = model.evaluate(X, y, verbose=0)
trainScore = math.sqrt(trainScore)
trainScore = scaler.inverse_transform(numpy.array([[trainScore]]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = model.evaluate(X_test, y_test, verbose=0)
testScore = math.sqrt(testScore)
testScore = scaler.inverse_transform(numpy.array([[testScore]]))
print('Test Score: %.2f RMSE' % (testScore))

