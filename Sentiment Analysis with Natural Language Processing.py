import pandas, numpy as np
import json,re
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import state_union, stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn import metrics
df=pandas.read_json("/Users/ankursharma/Desktop/Semester_1/Machine_Learning/project/dataset/review.json", orient="columns")

df[['stars']]=df[['stars']].replace([3],0)
df[['stars']]=df[['stars']].replace([1,2],0)
df[['stars']]=df[['stars']].replace([4,5],1)

#df[['text']]=df[['text']].replace(['\n'], ' ')

pattern = re.compile("[^a-zA-z\n]")
#print(df)
#for text in df[['text']]:
  #  output =re.sub(r'\d+', '',text)
 #   print(output, ' ', text)

list =[]
for i,text in enumerate(df['text']):
    output =re.sub(r'(\d+|_)', '',text)
    #output=output.replace('_','')
    list.append(output)
#print(list)
data=pandas.DataFrame(data=list, columns=["text"])

#print(df)

stopset = set(stopwords.words('english'))
vector = TfidfVectorizer(use_idf=True, lowercase=True, strip_accents='ascii', stop_words=stopset)

y = df.stars

x= vector.fit_transform(data.text)


vector.get_feature_names()


print(y.shape)
print(x.shape)

X_train, X_test, y_train, y_test = train_test_split(x,y,random_state=42)

clf = naive_bayes.MultinomialNB()
clf.fit(X_train, y_train)

roc_auc_score(y_test, clf.predict_proba(X_test)[:,1], average='weighted')




review = np.array(["worst place. Although it has average environment"])
print(review)


print(clf.predict(vector.transform(review)))

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
mlp = MLPClassifier(hidden_layer_sizes=(80,80),random_state=89, max_iter=35 ,solver='lbfgs', learning_rate='constant')
mlp.fit(X_train, y_train)

roc_auc_score(y_test, mlp.predict_proba(X_test)[:,1], average='weighted')




#scores = cross_val_score(mlp, A, B, cv=10)
#scores

from sklearn import tree
clf1 = tree.DecisionTreeClassifier(splitter='best', max_depth=7, min_samples_split=55, min_samples_leaf=52, max_features=None, random_state=70)
clf1.fit(X_train, y_train)
roc_auc_score(y_test, clf1.predict_proba(X_test)[:,1], average='weighted')