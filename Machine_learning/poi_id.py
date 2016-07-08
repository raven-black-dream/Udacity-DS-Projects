#!/usr/bin/python

import pickle
import numpy as np
import string
import re
# from email_parse import email_parse, email_data_finalize
from tester import test_classifier, dump_classifier_and_data
from feature_format import featureFormat, targetFeatureSplit
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.decomposition import PCA
from time import time
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import recall_score


# Task 1: Select what features you'll use.
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".

# removes unwanted words/items from the email line being parsed

t0 = time()
features_list = ['poi', 'salary', 'exercised_stock_options', 'deferral_payments', 'total_payments', 'other',
                 'bonus', 'restricted_stock', 'deferred_income', 'long_term_incentive', 'restricted_stock_deferred',
                 'percent_from_poi', 'percent_to_poi', 'total_stock_value', 'expenses', 'shared_receipt_with_poi',
                 'director_fees', 'loan_advances']

# Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset_modified.pkl", "r"))
# Task 2: Remove outliers
data_dict.pop("TOTAL", None)
# Data cleaning tasks
value = data_dict['BELFER ROBERT']['deferral_payments']
data_dict['BELFER ROBERT']['deferral_payments'] = 'NaN'
data_dict['BELFER ROBERT']['deferred_income'] = value
data_dict['BHATNAGAR SANJAY']['total_stock_value'] = 'NaN'

# Task 3: Create new feature(s)
for key in data_dict:

    # Creates a feature which is a percentage of emails to/from Persons of Interest
    if data_dict[key]['from_poi_to_this_person'] != "NaN" and data_dict[key]['to_messages'] != "NaN":
        data_dict[key]['percent_from_poi'] = float(data_dict[key]['from_poi_to_this_person']) /\
                                            float(data_dict[key]['to_messages'])
    else:
        data_dict[key]['percent_from_poi'] = 0
    if data_dict[key]['from_this_person_to_poi'] != "NaN" and data_dict[key]['from_messages'] != "NaN":
        data_dict[key]['percent_to_poi'] = float(data_dict[key]['from_this_person_to_poi']) /\
                                            float(data_dict[key]['from_messages'])
    else:
        data_dict[key]['percent_to_poi'] = 0

# Creates a list of the words in the emails sent to/from each person
print("Done in %0.3fs" % (time() - t0))

# email_parse(data_dict)

# Takes the pkl file which contains the email data and performs a percentile feature selection step
# with the intent of only getting the useful text features

# email_data_finalize()

# Load the dumped data
t0 = time()
print 'Loading Tf-IDf dictionary'
tfidf_dict = pickle.load(open('email_data.pkl', 'rb'))
print("Done in %0.3fs" % (time() - t0)) + "\nLoading List of Features"
list_of_features = pickle.load(open('list_of_features.pkl', 'rb'))
print("Done in %0.3fs" % (time() - t0))
# getting a list of the features which all pois and most nonpois have (in an effort to remove constant feature and
# divide by zero warnings

poi_relevant_features = []
for feature in tfidf_dict['METTS MARK'].keys():
    poi_count = 0
    npoi_count = 0
    for name in tfidf_dict:
        if tfidf_dict[name]['poi'] == True and tfidf_dict[name][feature] != 0.0:
            poi_count += 1
        if tfidf_dict[name]['poi'] == False and tfidf_dict[name][feature] != 0.0:
            npoi_count += 1
    if poi_count == 12 and npoi_count < 50:
        poi_relevant_features.append(feature)
list_of_features = (list(set(list_of_features) - set(poi_relevant_features)))
list_of_features.insert(0, 'poi')

for name in tfidf_dict:
    if tfidf_dict[name]['poi'] != 0.0 and tfidf_dict[name]['poi'] != 1:
        tfidf_dict[name]['poi'] = 0

data = featureFormat(tfidf_dict, list_of_features)
labels, features = targetFeatureSplit(data)
selector = SelectKBest(k=50)
# When selector was select k best - k = 50: Accuracy = 0.9082, Precision = 0.83676, Recall = 0.387
# When selector was select percentile - percentile = 10: Acc =0.83733 , Pre = 0.24419 , Rec = 0.105
# This is a significant decrease
# When Selector was select precentile - percentile = 5: Acc =0.83773 , Pre = 0.21144 , Rec = 0.07950
# This was another significant decrease


selector.fit(features, labels)

selected = selector.get_support()
list_of_features.pop(0)
list_of_features = np.array(list_of_features)
selected_features = list_of_features[selected]
for feature in selected_features:
    print feature
remove = set(list_of_features) - set(selected_features)

for key in tfidf_dict.keys():
    tfidf_dict[key].pop('poi', None)

for key in tfidf_dict.keys():
    for feature in remove:
        tfidf_dict[key].pop(feature, None)
    data_dict[key].update(tfidf_dict[key])
empty_set = {}
for key in tfidf_dict['METTS MARK'].keys():
    empty_set[key] = 0.0

for key in data_dict:
    if len(data_dict[key]) == 23:
        data_dict[key].update(empty_set)

# Changes 'NaN' values to 0.0 and with the exception of certain features performs a Min Max Scaling
for name in data_dict:
    for item in data_dict[name].keys():
        if data_dict[name][item] == 'NaN':
            data_dict[name][item] = 0.0
# Store to my_dataset for easy export below.
my_dataset = data_dict
selected_features = list(selected_features)
selected_features.extend(features_list)
selected_features.remove('poi')
selected_features.insert(0, 'poi')
# Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, selected_features, sort_keys=True)
labels, features = targetFeatureSplit(data)

# Task 4: Try a varity of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html
'''
pipeline = Pipeline([('scaling', MinMaxScaler()),
                     #('feature_selection', SelectKBest()),
                     ('pca', PCA()),
                     ('neighbours', KNeighborsClassifier())])
parameters = {#'feature_selection__k': ['all', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
              'pca__n_components': [None, 1, 2, 3, 4, 5, 6, 7, 8, 9],
              'pca__whiten': [True, False],
              'neighbours__n_neighbors': [1, 2, 3, 4, 5, 6, 7],
              'neighbours__algorithm': ['ball_tree', 'kd_tree', 'brute'],
              'neighbours__weights': ['uniform', 'distance'],
              'neighbours__leaf_size': [1, 2, 3, 7, 10, 20, 25, 30, 35]}
# Using Grid Search to tune parameters.

print ("Test 1:")
gridsearch = GridSearchCV(pipeline, parameters, scoring='recall', cv=StratifiedShuffleSplit(labels))
t0 = time()
gridsearch.fit(np.array(features), np.array(labels))
print("done in %0.3fs" % (time() - t0))
print gridsearch.best_score_
best_parameters = gridsearch.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))
# applied the above parameters to the estimator for testing
'''
clf = make_pipeline(MinMaxScaler(), PCA(n_components=4, whiten=True),
                    KNeighborsClassifier(algorithm='kd_tree', leaf_size=3, n_neighbors=1, weights='uniform'))

test_classifier(clf, my_dataset, selected_features)
# Accuracy = 0.91547, Precision = 0.76599, Recall = 0.527

print ("Test 2:")
'''
pipeline = Pipeline([('dt', DecisionTreeClassifier())])
parameters = {'dt__criterion': ('gini', 'entropy'), 'dt__max_features': (0.05, 0.10, 0.15, 0.20, 'sqrt', 'log2'),
              'dt__min_samples_split': (1, 2, 3, 4, 5), 'dt__min_samples_leaf': (1, 2, 3, 4, 5),
              'dt__class_weight': (None, 'balanced'), 'dt__presort': (False, True)}

gridsearch = GridSearchCV(pipeline, parameters, cv=StratifiedShuffleSplit(labels))
t0 = time()
gridsearch.fit(np.array(features), np.array(labels))
print("done in %0.3fs" % (time() - t0))
best_parameters = gridsearch.best_estimator_.get_params()
print gridsearch.best_score_
for param_name in sorted(parameters.keys()):
   print("\t%s: %r" % (param_name, best_parameters[param_name]))
'''
clf2 = make_pipeline(DecisionTreeClassifier(class_weight=None, criterion='entropy', max_features=0.05,
                                           min_samples_leaf=1, min_samples_split=5, presort=False))
test_classifier(clf2, my_dataset, selected_features)
# Accuracy = 0.8648, Precision = 0.48997, Recall = 0.342
print ("Test 3:")
'''
pipeline = Pipeline([('Scaler', MinMaxScaler()), ('SVC', SVC())])
parameters = {'SVC__kernel': ['rbf', 'linear', 'poly'], 'SVC__C': [1, 10, 100, 1000], 'SVC__max_iter': [-1, 5, 10, 15],
               'SVC__degree': [2, 3, 4,]}

gridsearch = GridSearchCV(pipeline, parameters, cv=StratifiedShuffleSplit(labels))
t0 = time()
gridsearch.fit(np.array(features), np.array(labels))
print("done in %0.3fs" % (time() - t0))
best_parameters = gridsearch.best_estimator_.get_params()
print gridsearch.best_score_
for param_name in sorted(parameters.keys()):
   print("\t%s: %r" % (param_name, best_parameters[param_name]))
'''
clf3 = make_pipeline(MinMaxScaler(), SVC(C=10, kernel='rbf', max_iter=15))
test_classifier(clf3, my_dataset, selected_features)
# Accuracy = 0.91333, Precision = 0.76718, Recall = 0.5025

# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script.
# Because of the small size of the dataset, the script uses stratified
# shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

#test_classifier(clf, my_dataset, features_list)

# Dump your classifier, dataset, and features_list so
# anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)
