import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn import tree

df = pd.read_csv('./train.csv');

df.drop(['Id'], inplace=True, axis=1)

df = df.join(pd.get_dummies(df['MSZoning']))
df.drop(['MSZoning'], inplace=True, axis=1)

df.fillna(df['LotFrontage'].mean(), inplace=True)

df.drop(['Alley'], inplace=True, axis=1)

df = df.join(pd.get_dummies(df['LotShape']))
df.drop(['LotShape'], inplace=True, axis=1)

print df.head()
exit()
# import a dataset
train_data = []
train_target = []
with open('train.csv', 'rb') as csvfile:
    file_reader = csv.reader(csvfile, delimiter=',')
    train_data1 = list(file_reader)[1:]
    for row in train_data1:
        r = []
        train_target.append(row[-1])
        del row[-1]
        for a in row:
            try:
                r.append(float(a))
            except:
                r.append(data_def_dict[a.lower()])
        train_data.append(r)

test_data = []
test_target = []
with open('test.csv', 'rb') as csvfile:
    file_reader = csv.reader(csvfile, delimiter=',')
    test_data1 = list(file_reader)[1:]
    for row in train_data1:
        r = []
        for a in row:
            try:
                r.append(float(a))
            except:
                r.append(data_def_dict[a.lower()])
        test_data.append(r)


train_data, test_data,train_target, test_target = train_test_split(train_data, train_target, test_size=.5)
print len(train_data)
print len(train_target)
print len(test_data)
print len(test_target)
# exit()
# my_classifier = tree.DecisionTreeClassifier()
# my_classifier = GaussianNB()
# my_classifier = SGDClassifier(loss="hinge", penalty="l2")
# my_classifier = KNeighborsClassifier()
# my_classifier = gaussian_process.GaussianProcess()
# my_classifier = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5)
# my_classifier = RandomForestClassifier()
# my_classifier = ExtraTreesClassifier()
# my_classifier = tree.DecisionTreeClassifier()
# my_classifier = MultiLabelBinarizer()
# my_classifier = OneVsOneClassifier(LinearSVC(random_state=0))

my_classifier.fit(train_data, train_target)

prediction = my_classifier.predict_proba(test_data)
# print prediction

print accuracy_score(test_target, prediction)
