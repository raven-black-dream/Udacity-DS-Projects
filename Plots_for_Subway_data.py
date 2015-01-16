
# coding: utf-8

# In[1]:

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

subway_data = pandas.read_csv(f1)

sd_with_rain = subway_data[subway_data['rain']==1].groupby(['station'], as_index = False).mean()
sd_with_rain = sd_with_rain.sort(['ENTRIESn_hourly'], ascending = False)
sd_with_rain = sd_with_rain[sd_with_rain['ENTRIESn_hourly'] >= 6000]
sd_with_rain = sd_with_rain.reset_index(drop = True)
sd_with_rain

sd_without_rain = subway_data[subway_data['rain']==0].groupby(['station'], as_index = False).mean()
sd_without_rain = sd_without_rain.sort(['ENTRIESn_hourly'], ascending = False)
sd_without_rain = sd_without_rain[sd_without_rain['ENTRIESn_hourly'] >= 6000]
sd_without_rain = sd_without_rain.reset_index(drop = True)
sd_without_rain

ggplot(sd_with_rain, aes(x = 'station', y = 'ENTRIESn_hourly'))\
+ geom_bar(aes(weight = 'ENTRIESn_hourly', fill = "blue", color = "steelblue"), stat = "bar")\
+ geom_bar(aes(weight = 'ENTRIESn_hourly'), data = sd_without_rain, stat = "bar")\
+ theme(axis_text_x = element_text(angle = 45, hjust = 1, size = 6, color = "black", vjust = 1))\
+ ggtitle("Busiest Stations on Rainy and Non-rainy days") + xlab("Station") + ylab("Average Entries per Hour")



