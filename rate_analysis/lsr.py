import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn import linear_model
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
# #
# print len(X_test)
# print X
# print len(y_test)
# exit()

model = linear_model.BayesianRidge()
model.fit(X, y)
predicted = model.predict(X_test)
# print model.predict_proba(X_test)
a = np.mean(predicted)
b = np.mean(y_test)
print a
print b
print (a-b)/b

# print model.predict([10, 30,2016,])
# exit()
original_diff = np.absolute(np.subtract(predicted, y_test))
diff = np.array(original_diff)
print "-- With include Zeros -- "
print "min diff ", np.min(diff)
print "max diff ", np.max(diff)
print "Mean diff ",np.mean(diff)

print "\n"

print "-- With exlude Zeros -- "
diff = diff[diff!=0]
print "min diff ", np.min(diff)
print "max diff ", np.max(diff)
print "Mean diff ",np.mean(diff)

print "\n"

print "accuracy ", model.score(X_test, y_test)

# exit()
fig = plt.figure()
plt.plot(predicted, label="Predicted")
plt.plot(y_test, label="Original")
plt.plot(original_diff, label="diff")
plt.legend(loc="upper left")
# plt.plot(df_year['index'], df_year['Modal Price'], label="Year")
# plt.plot(df_month['index'], df_month['Modal Price'], label="Month")
# plt.plot(df_week['index'], df_week['Modal Price'], label="Week")
# plt.plot(df_day['index'], df_day['Modal Price'], label="Day")
# plt.scatter(df['Year'], df['Modal Price'])
# plt.plot_date(df['index'], df['Modal Price'])
plt.show()

# print df['Price Date']
