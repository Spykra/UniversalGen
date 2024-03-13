import numpy as np

def detect_outliers(df, column):
    Q1 = np.percentile(df[column], 25, interpolation='midpoint')
    Q3 = np.percentile(df[column], 75, interpolation='midpoint')
    IQR = Q3 - Q1

    # Define bounds for outliers
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    # Return a new DataFrame with outliers removed
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
