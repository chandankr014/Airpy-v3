import pandas as pd
import numpy as np


# OUTLIER DETECTION AND REMOVAL 

def detect_outliers(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers


# MISSING VALUES SUMMARY
def missing_data_summary(data):
    missing_values = data.isnull().sum()
    missing_percentage = (missing_values / len(data)) * 100

    # Display missing data summary
    missing_data_summary = pd.DataFrame({'Missing Values': missing_values, 'Percentage': missing_percentage})
    print("Missing Data Summary:\n", missing_data_summary)