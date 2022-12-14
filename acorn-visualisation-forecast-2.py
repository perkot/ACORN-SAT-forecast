# #%%

# /* ------------------------------------------------- /*
# NAME: ACORN-SAT (time-series)
# PURPOSE : data-set to practice time-series analysis 
# DATE : 14/11/2022
# AUTHOR : TOM PERKINS
# /* ------------------------------------------------- */

# -------------------------------------------
# DEPENDENCIES 
# -------------------------------------------

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# -------------------------------------------
# READ DATA 
# -------------------------------------------

# Aus temperature data : 1910 - 2019 
acorn = pd.read_csv(r"/Users/perkot/GIT/data/ACORN-SAT-Clean.csv")
# Global CO2 data : 1756 : 2020
co2 = pd.read_csv(r"/Users/perkot/GIT/data/owid-co2-data.csv")

# /* ------------------------------------------------- */
# ACORN-SAT
# /* ------------------------------------------------- */

# -------------------------------------------
# SUMMARISE
# -------------------------------------------

# column names 
acorn.columns.values
# summary of df
acorn.describe
# get variable types of all columns 
acorn.dtypes
# print
print(acorn)
# unique years
acorn.Year.unique()

# -------------------------------------------
# TIDY
# -------------------------------------------

# rename columns 
acorn = acorn.rename(columns={'maximum temperature (degC)': 'max_temp', 'minimum temperature (degC)': 'min_temp'})

# -------------------------------------------
# SUBSET
# -------------------------------------------

acorn_sub = acorn.loc[acorn['Year'] <= 2018]

acorn_sub.tail(20)

# -------------------------------------------
# SUMMARISE AVERAGES 
# -------------------------------------------

# This calculates group means 
    # double brackets to ensure a df 
    # also need to include both grouping variables in mean calculation  
    # https://stackoverflow.com/questions/46938572/pandas-groupby-mean-into-a-dataframe
    # acorn_avg = acorn.groupby(['State', 'Year'])['max_temp'].mean().reset_index

acorn_avg =  acorn_sub.groupby(['Yr_Month', 'Year'], as_index = False).mean()[['Yr_Month', 'Year', 'max_temp']]

# print
print(acorn_avg)

# -------------------------------------------
# PIVOT
# -------------------------------------------

# pivot 
# acorn_avg_p = pd.pivot_table(acorn_avg, values = 'max_temp', index=['Yr_Month'], columns = 'State').reset_index()
# print
# print(acorn_avg_p)

# https://data.worldbank.org/indicator/EN.ATM.CO2E.PC?locations=AU
# https://github.com/owid/co2-data

# /* ------------------------------------------------- */
# CO2
# /* ------------------------------------------------- */

# -------------------------------------------
# SUMMARISE 
# -------------------------------------------

# unique years
co2.year.unique()
# print
print(co2)

# -------------------------------------------
# TIDY
# -------------------------------------------

# subset
co2 = co2[["country", "year", "co2"]]

# yearly average 
co2_avg =  co2.groupby(['year'], as_index = False).mean()[['year', 'co2']]

print(co2_avg)

# Around 1950 things begin to spike -- might be interesting to try and forecast 
co2_avg.plot(x="year", y="co2")
# plt.ylim([10, 40])
plt.xticks('year', l)
plt.ylabel('avg co2')
plt.show()

# goal is to re-index these average values to monthly 

# convert year into date format 
co2_avg['year'] = pd.to_datetime(co2_avg['year'], format='%Y')

co2_avg = co2_avg.loc[co2_avg['year'] >= '1910-01-01'] 
co2_avg = co2_avg.loc[co2_avg['year'] <= '2019-12-01']

print(co2_avg)

# re-index yearly average to a monthly average, spread evenly across the 12 months of the year 
co2_avg_m =  co2_avg.set_index('year').resample('M').bfill().reset_index()

# check 
print(co2_avg_m)

# create yr-month column from date
co2_avg_m['yr-month'] = co2_avg_m['year'].dt.strftime('%Y-%m')

# subset
co2_avg_m = co2_avg_m[["yr-month", "co2"]]

# co2.avg["monthly_co2"] = co2.avg["co2"] / co2_avg.index.monthsinyear

co2_avg_m.tail(20)

# /* ------------------------------------------------- */
# JOIN
# /* ------------------------------------------------- */

# left join on single id
acornco2 = acorn_avg.merge(co2_avg_m, left_on='Yr_Month', right_on='yr-month', how = "left").drop(columns = ['Year', 'yr-month'])

acornco2.tail(20)

print(acornco2)

# Export 
# acornco2.to_csv(r"/Users/perkot/GIT/data/acornco2.csv", index = False)
# Import 
acornco2 = pd.read_csv(r"/Users/perkot/GIT/data/acornco2.csv")

print(acornco2)

# -------------------------------------------
# VISUALIZE 
# -------------------------------------------

# ------
# Simple plot
# ------
# acorn_avg.plot(x="Yr_Month", y="max_temp")
# plt.ylim([10, 40])
# plt.xticks('Yr_Month', l)
# plt.ylabel('daily max temperature')
# plt.show()

# ------
# Plot with aesthetics 
# ------

# WORKING
# ----------------------------------------------
# ------
# Colour scheme
# ------

GREY10 = "#1a1a1a"
GREY30 = "#4d4d4d"
GREY40 = "#666666"
GREY50 = "#7f7f7f"
GREY60 = "#999999"
GREY75 = "#bfbfbf"
GREY91 = "#e8e8e8"
GREY98 = "#fafafa"
BLUE01 = "#308ed1"
BLUE02 = "#7AA2BE"

# ------
# # Initialize layout
# ------

# ----------------------------------------------
fig, ax = plt.subplots(figsize = (14, 8.5))
# ----------------------------------------------
type(fig)
# matplotlib.figure.Figure
type(ax)
# matplotlib.axes._subplots.AxesSubplot
# ----------------------------------------------

# Background color
fig.patch.set_facecolor(GREY98)
ax.set_facecolor(GREY98)

# ------
# GRID
# ------

ax.yaxis.grid(True, which='major', color=GREY91)
ax.xaxis.grid(True, which='major', color=GREY60)

# ------
# Y AXIS
# ------

# limit range of y values 
ax.set_ylim(10, 35)
ly = ['10', '15', '20', '25', '30', '35'] 
# add y-axis labels to plot 
ax.set_yticklabels(ly, fontname= "Montserrat", fontsize=13, weight=500, color=GREY40) 

# ------
# X AXIS
# ------

# how many ticks on x-axis 
ax.xaxis.set_major_locator(plt.MaxNLocator(13)) # specify 11 levels on the x-axis 
# custom levels
l = ['', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'] 
# add x-axis labels to plot  
ax.set_xticklabels(l, fontname= "Montserrat", fontsize=13, weight=500, color=GREY40) 

# change y label 
ax.set_ylabel('daily max temperature', fontname= "Montserrat", fontsize=13, weight=500, color=GREY40)
# move away from axis
ax.yaxis.set_label_coords(-0.05,0.5)

# ------
# TITLE
# ------

fig.text(
    0.18,
    0.92,
    "Time Series showing monthly average of daily-maximum temperature from 1910 to 2016",
    color=GREY10,
    fontsize=14,
    fontname="Montserrat",
    weight="bold")

# ------
# plot
# ------

for data in acorn_avg:
    data = acorn_avg
    ax.plot("Yr_Month", "max_temp", color=BLUE01, lw=1.2, alpha=0.5, data=data)
    
# ------
# SHOW
# ------

plt.show()

# /* ------------------------------------------------- */
# TIME SERIES
# /* ------------------------------------------------- */

# Plan

# Train = 1950-1989
# Test = 1990-2018

acornco2 = acornco2.loc[acornco2['Yr_Month'] >= '1950-01'] 

train = acornco2.loc[acornco2['Yr_Month'] < '1990-01']
print(train)
test = acornco2.loc[acornco2['Yr_Month'] >= '1990-01']
print(test)

# https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/

# plotting actual v predicted
# https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/

# https://www.datacamp.com/tutorial/tutorial-time-series-forecasting

# aim to do sarimax
# seasonal + exogenous variable co2

# https://towardsdatascience.com/time-series-forecast-in-python-using-sarimax-and-prophet-c970e6056b5b

import statsmodels.api as sm
from pylab import rcParams

# https://www.statsmodels.org/stable/index.html

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(acorn_avg["max_temp"], model='additive', period = 30)
fig = decomposition.plot()
plt.show()


# ----------------------------------------------
# END

# -------------------------------------------
# REFERENCES 
# -------------------------------------------

# https://towardsdatascience.com/what-are-the-plt-and-ax-in-matplotlib-exactly-d2cf4bf164a9
# https://www.python-graph-gallery.com/web-line-chart-with-labels-at-line-end
# https://realpython.com/pandas-plot-python/
# https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots-in-matplotlib-pyplot-python
# https://stackoverflow.com/questions/46938572/pandas-groupby-mean-into-a-dataframe
# https://stackoverflow.com/questions/45306105/pandas-convert-yearly-to-monthly