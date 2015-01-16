# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 13:17:06 2014

@author: Evan
"""
import pandas
from ggplot import *
import numpy as np
import scipy
import scipy.stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import datetime
import time
pandas.options.mode.chained_assignment = None

    
f1 = "C:/Users/Evan/Downloads/turnstile_weather_v2.csv"
f2 = "C:/Users/Evan/Downloads/turnstile_data_master_with_weather.csv"


def subway_data_analysis(filename):
    subway_data = pandas.read_csv(filename)
    with_rain = subway_data['ENTRIESn_hourly'][subway_data['rain'] == 1]
    without_rain = subway_data['ENTRIESn_hourly'][subway_data['rain'] == 0]
    mean_with_rain = np.mean(with_rain)
    mean_without_rain = np.mean(without_rain)
    U, p = scipy.stats.mannwhitneyu(with_rain, without_rain)
    print("Mean with Rain: ", mean_with_rain)
    print("Mean without Rain: ", mean_without_rain)
    print("U value: ", U, "and p value: ", p)
    
    prediction = predictions(subway_data)
    r_squared = compute_r_squared(subway_data['ENTRIESn_hourly'], prediction)
    subway_data['prediction'] = prediction    
    print("R^2 value: ", r_squared)
    #plot_subway_data(subway_data)
    
    
#def plot_subway_data(subway_data):
    
    #print(plot)
    #return plot  
    
def compute_r_squared(data, predictions):
    '''
    In exercise 5, we calculated the R^2 value for you. But why don't you try and
    and calculate the R^2 value yourself.
    
    Given a list of original data points, and also a list of predicted data points,
    write a function that will compute and return the coefficient of determination (R^2)
    for this data.  numpy.mean() and numpy.sum() might both be useful here, but
    not necessary.

    Documentation about numpy.mean() and numpy.sum() below:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
    '''

    mean = np.mean(data)
    numerator = ((data - predictions)**2).sum()
    denominator = ((data - mean)**2).sum()
    r_squared = 1 - numerator/denominator
    
    return r_squared


def predictions(turnstile_weather):
    
    
    ols_regression = smf.ols(data = turnstile_weather, formula = "ENTRIESn_hourly ~ datetime+weekday+station+conds+fog+meanprecipi+meanpressurei+meantempi+meanwspdi+hour").fit()
    prediction = ols_regression.predict()
     
    return prediction
    
subway_data_analysis(f1)