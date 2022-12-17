# ForecastingElectricityUsage

## Group 2



### Problem Statement

Electricity use varies over time of day, month, year due to various factors. Can we predict this use solely from the datetime data? The objective here is to predict electricity load in kW for a given datetime.



#### Data

Contains the electricity load of 370 anonymous users (in kW) for each 15-minute interval2011 to 2014 Training set: 2011-01-01 - 2014-03-31Test set: 2014-04-01 - 2014-12-31Aggregates 15 minutes to daily load (downsizing samples) Expands with features for each user (ex. lags, means, standard deviations, year, month, etc.) Normalize by each user’s mean and standard deviationClusters to groups based on the features



#### Models

- XGBoost
- Random Forest
- LSTM
- ARIMA
- Facebook Prophet
- DeepAR



#### Methods:

We divided data into train and 3 test sets. We used the training data to learn patterns in the data and used the test sets to validate forecasts. Across all 370 users, we tried to find the best models, but in some cases the users' data is not plausible and might represent outliers, so those were disregarded. Finally, we evaluated models based on **Mean Absolute Percentage Error (MAPE)**



#### Results:

- ARIMA models seem to perform best on average across all 3 time horizons.
- Previous implementations suggested XGBoost performed well, but that was hampered by data leakages which nullify the results.