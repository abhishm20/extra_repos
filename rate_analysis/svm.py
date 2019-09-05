import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd


###############################################################################
# Generate sample data
# Read CSV
df = pd.read_csv('./potato_rates.csv')


# Filter by market
df = df[df['Market Name'].isin(['Azadpur'])]


# Change values to float
df['Modal Price'] = df['Modal Price'].astype('int')
df['Max Price'] = df['Max Price'].astype('int')
df['Min Price'] = df['Min Price'].astype('int')
df['Price Date'] = df['Price Date'].astype('string')

df['Price Date'] = pd.to_datetime(df['Price Date'])


# Remove Outliers
mean = np.mean(df['Modal Price'])
std = np.std(df['Modal Price'])
df = df[abs(df['Modal Price'] - mean) <= 5*np.std(df['Modal Price'])]
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

###############################################################################
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
# svr_lin = SVR(kernel='linear', C=1e3)
# svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X_test)
# y_lin = svr_lin.fit(X, y).predict(X_test)
# y_poly = svr_poly.fit(X, y).predict(X_test)

###############################################################################
# look at the results
plt.plot(X_test, y_test, c='k', label='data')
# plt.hold('on')
plt.plot(X_test, y_rbf, c='g', label='RBF model')
# plt.plot(X_test, y_lin, c='r', label='Linear model')
# plt.plot(X_test, y_poly, c='b', label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()