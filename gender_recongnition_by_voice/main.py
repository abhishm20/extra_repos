# import a dataset
import csv
with open('voice.csv', 'rb') as csvfile:
    file_reader = csv.reader(csvfile, delimiter=',')
    dataset = list(file_reader)

data = []
target = []
for row in dataset:
    target.append(row[-1])
    del row[-1]
    data.append(row)

data = [[float(i) for i in row] for row in data[1:]]
target = [(1 if a == 'male' else 0) for a in target[1:]]

# import data_split lib
from sklearn.cross_validation import train_test_split
test_data, train_data, test_target, train_target = train_test_split(data, target, test_size=.5)

# import learning lib

from scipy.spatial import distance

class MyFirstClassifier:
    def fit(self, test_data, test_target):
        self.train_data = train_data
        self.train_target = train_target

    def predict(self, test_data):
        prediction = []
        for row in test_data:
            closer = self.closest(row)
            prediction.append(closer)
        return prediction

    def closest(self, row):
        min_index = 0
        min_dis = distance.euclidean(row, self.train_data[0])
        for i in range(0, len(self.train_data)):
            dis = distance.euclidean(row, self.train_data[i])
            if dis < min_dis:
                min_dis = dis
                min_index = i
        return self.train_target[min_index]


from sklearn.neighbors import KNeighborsClassifier
my_classifier = KNeighborsClassifier()

# from sklearn import tree
# my_classifier = tree.DecisionTreeClassifier()

# My Classifier
# my_classifier = MyFirstClassifier()

my_classifier.fit(train_data, train_target)

prediction = my_classifier.predict(test_data)

from sklearn.metrics import accuracy_score
print accuracy_score(prediction, test_target)
