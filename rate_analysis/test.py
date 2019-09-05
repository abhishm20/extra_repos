import csv
import numpy as np
from sklearn.svm import SVR
from sklearn import linear_model
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from datetime import datetime


dates = []
prices = []


def get_data(filename):
    with open(filename,'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader) #skipping column names
        for row in csvFileReader:
            dates.append([int(datetime.strptime(row[8], "%d-%b-%y").strftime("%s"))])
            prices.append(float(row[7])/100)
    return


# def show_plot(dates,prices):
#     linear_mod = SVR(kernel='rbf', C=1e3, gamma=0.1)
#     linear_mod.fit(dates,prices) #fitting the data points in the model
#     plt.scatter(dates,prices,color='yellow') #plotting the initial datapoints
#     plt.plot(dates,linear_mod.predict(dates),color='blue',linewidth=3) #plotting the line made by linear regression
#     plt.show()
#     return


def predict_price(dates,prices,x):
    linear_mod = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # linear_mod = linear_model.LinearRegression() #defining the linear regression model
    # dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    # prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    predicted_price =linear_mod.predict([[x]])
    return predicted_price[0]
    # return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]

get_data('./onion_rates.csv') # calling get_data method by passing the csv file to it
# print dates[0][0]
# print prices[0]
# print "\n"
#
# show_plot(dates,prices)
# exit()

# predicted_price = predict_price(dates,prices,int(datetime.now().strftime("%f")))
predicted_price = predict_price(dates,prices,int(datetime.strptime('26-Sep-16', "%d-%b-%y").strftime("%s")))
print "Todays Rate is ", str(predicted_price)
