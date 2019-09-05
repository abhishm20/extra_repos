import numpy, math
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

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

#----------
# build the network
#----------

from sklearn.neural_network import MLPRegressor
clf = MLPRegressor(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y)
predicted = clf.predict(X_test)
#----------
# evaluate
#----------
import pylab
# neural net approximation

# target function
pylab.plot(X_test,
           y_test, linewidth= 2, color= 'red', label = 'actual')
pylab.plot(X_test,
           predicted, linewidth= 2, color= 'green', label = 'target')
pylab.legend()
pylab.show()
