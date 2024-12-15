import pandas as pd
import numpy as np
import os

def fetch_data(url, path, name):
    """
    Fetches a dataset from a given URL, saves it to a specified path with a specified name.

    Args:
        url (str): The URL to download the dataset from.
        path (str): The local directory where the file should be saved.
        name (str): The name of the file (without extension) to save the dataset as.

    Returns:
        None
    """
    if not os.path.exists(path):
        os.makedirs(path)

    data = pd.read_csv(url)
    data.to_csv(f"{path}/{name}.csv", index=False)

    print(f"Dataset downloaded and saved as {name}.csv.")

def detect_outliers(df):
    """
    Detects outliers in numerical columns based on the IQR method.

    Args:
        df (pandas.DataFrame): The input dataframe containing the data to check for outliers.

    Returns:
        dict: A dictionary with column names as keys and the corresponding rows with outliers as values.
    """
    outliers = {}
    for column in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers[column] = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    return outliers

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