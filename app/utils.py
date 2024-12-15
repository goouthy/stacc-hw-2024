import pandas as pd
import numpy as np

def fetch_data(url):
    """
    Fetches a dataset from a given URL and loads it into a Pandas DataFrame.

    Args:
        url (str): The URL to download the dataset from.

    Returns:
        pd.DataFrame: The dataset as a Pandas DataFrame.
    """
    df = pd.read_csv(url)
    print("Dataset downloaded and loaded into a DataFrame.")
    return df

def remove_outliers(df):
    """
    Removes outliers from a DataFrame based on the Interquartile Range (IQR) rule.

    Args:
        df (pandas.DataFrame): The input DataFrame from which outliers need to be removed.

    Returns:
        pandas.DataFrame: The DataFrame with outliers removed.
    """
    for column in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df