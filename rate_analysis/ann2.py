from pybrain.datasets import SupervisedDataSet
import numpy, math
import pandas as pd
import numpy as np

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





ds = SupervisedDataSet(4, 1)
for x, y in zip(X, y):
    ds.addSample(x, y)

#----------
# build the network
#----------
from pybrain.structure import TanhLayer, LinearLayer, LSTMLayer
from pybrain.tools.shortcuts import buildNetwork

net = buildNetwork(4,
                   30, # number of hidden units
                   1,
                   bias = True,
                   hiddenclass = TanhLayer,
                   outclass = LinearLayer
                   )
#----------
# train
#----------
from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds,learningrate=0.01, momentum=0.1, verbose = True)
trainer.trainUntilConvergence(maxEpochs = 100)

#----------
# evaluate
#----------
import pylab
# neural net approximation
pylab.plot(X,
           [ net.activate([x]) for x in X ], linewidth = 2,
           color = 'blue', label= 'NN output')

# target function
pylab.plot(X_test,
           y_test, linewidth= 2, color= 'red', label = 'target')

pylab.grid()
pylab.legend()
pylab.show()
