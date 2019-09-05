# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sklearn import tree
import pandas as pd
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split
import graphviz


df = pd.read_csv('data.csv')

df['status'].replace(['accepted', 'rejected'], [1, 0], inplace=True)
df['cibil score'].replace([-1], [650], inplace=True)
df['residence_type'].replace(['rented', 'owned'], [0, 1], inplace=True)
df['office_premises'].replace(['rented', 'owned'], [0, 1], inplace=True)

df = df.drop(['system_status', 'suggested_status', 'interest_rate', 'ratings', 'ls_credit_score', 'diff', 'current_state'], axis=1)
y = df.pop('status')

df = df.fillna(0)


clf = tree.DecisionTreeRegressor()
clf = clf.fit(df, y)

dot_data = tree.export_graphviz(clf, out_file=None, feature_names=df.columns,
                         class_names=['status'])
graph = graphviz.Source(dot_data)
graph.render()