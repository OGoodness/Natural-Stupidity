import pandas as pd
import os
import numpy as np
from sklearn import tree
import graphviz


import os
os.environ["PATH"] += os.pathsep + 'C:/Users/rcwie/Desktop/release/bin'
df = pd.read_csv("Titanic_training.csv")
td = pd.read_csv("Titanic_test.csv")


# Replacing Sex
df.Sex = df.Sex.replace('male', 0)
df.Sex = df.Sex.replace('female', 1)

td.Sex = td.Sex.replace('male', 0)
td.Sex = td.Sex.replace('female', 1)


# Replacing Age
df.Age = df.Age.fillna(30)
df.Age = df.Age.astype(np.int64)

td.Age = td.Age.fillna(30)
td.Age = td.Age.astype(np.int64)

# Replacing Fare
df.Fare = df.Fare.astype(np.int64)

td.Fare = td.Fare.fillna(0)
td.Fare = td.Fare.astype(np.int64)

# Replacing Embarked
df.Embarked = df.Embarked.replace('S', 0)
df.Embarked = df.Embarked.replace('C', 1)
df.Embarked = df.Embarked.replace('Q', 2)
df.Embarked = df.Embarked.fillna(3)
df.Embarked = df.Embarked.astype(np.int64)

td.Embarked = td.Embarked.replace('S', 0)
td.Embarked = td.Embarked.replace('C', 1)
td.Embarked = td.Embarked.replace('Q', 2)
td.Embarked = td.Embarked.fillna(3)
td.Embarked = td.Embarked.astype(np.int64)

# Drops Survived, PassengerId, Cabin, Name, Ticket (PassId, Cabin, Name, And Ticket are bad data)
data = df.drop(columns={'Survived', 'PassengerId', 'Cabin', 'Name', 'Ticket'}, axis=1)
tabledata = td.drop(columns={'PassengerId', 'Cabin', 'Name', 'Ticket'}, axis=1)

clf = tree.DecisionTreeClassifier()
clf.fit(data, df.Survived)
result = clf.predict(tabledata)
info = clf.tree_.node_count

result = pd.Series(result)
result.to_csv('output.csv', header='Survived')

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data, 'table')
graph.format = 'pdf'
graph.render()

print("Number of Nodes: " + str(clf.tree_.node_count))
print("Number of Leaf Nodes: " + str(clf.tree_.n_leaves))
