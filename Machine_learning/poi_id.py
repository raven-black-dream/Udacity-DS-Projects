#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def scale_features(min_val, max_val, num_val):
    scaled_number = ((num_val - min_val) / (max_val - min_val)) / (max_val - min_val) + min_val
    return scaled_number

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'exercised_stock_options', 'deferral_payments', 'total_payments', 'other',
                 'bonus', 'restricted_stock', 'deferred_income', 'long_term_incentive','restricted_stock_deferred',
                 'percent_from_poi', 'percent_to_poi' , 'total_stock_value', 'expenses', 'shared_receipt_with_poi']
### Load the dictionary containing the dataset
data_dict = pickle.load(open("final_project_dataset.pkl", "r") )
### Task 2: Remove outliers
data_dict.pop("TOTAL", None)
value = data_dict['BELFER ROBERT']['deferral_payments']
data_dict['BELFER ROBERT']['deferral_payments'] = 'NaN'
data_dict['BELFER ROBERT']['deferred_income'] = value
### Task 3: Create new feature(s)
for key in data_dict:

    if data_dict[key]['from_poi_to_this_person'] != "NaN" and data_dict[key]['to_messages'] != "NaN":
        data_dict[key]['percent_from_poi'] = float(data_dict[key]['from_poi_to_this_person'])/\
                                            float(data_dict[key]['to_messages'])
    else:
        data_dict[key]['percent_from_poi'] = 0
    if data_dict[key]['from_this_person_to_poi'] != "NaN" and data_dict[key]['from_messages'] != "NaN":
        data_dict[key]['percent_to_poi'] = float(data_dict[key]['from_this_person_to_poi'])/\
                                            float(data_dict[key]['from_messages'])
    else:
        data_dict[key]['percent_to_poi'] = 0

for item in features_list:
    if item == 'poi' or item == 'percent_from_poi' or item == 'percent_to_poi':
        continue
    else:
        feature_values = []
        for name in data_dict:
            if data_dict[name][item] != 'NaN':
                feature_values.append(float(data_dict[name][item]))
            else:
                feature_values.append(0.0)
                data_dict[name][item] = 0.0
        feature_values.sort()
        minimum_value = feature_values[0]
        maximum_value = feature_values[len(feature_values) - 1]

        for person in data_dict:
            data_dict[name][item] = scale_features(minimum_value, maximum_value, data_dict[name][item])

i = 0
for name in data_dict:
    if data_dict[name]['poi'] == 1:
        i += 1
print i
### Store to my_dataset for easy export below.
my_dataset = data_dict
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

clf = make_pipeline(PCA(n_components= 10), KMeans(n_clusters=8))

### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

test_classifier(clf, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)



