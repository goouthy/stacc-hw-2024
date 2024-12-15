# Iris Dataset Analysis and Web API
##### Homework for STACC Data Engineer position

This project covers the steps from fetching the classic Iris dataset, cleaning it, and serving it through a simple web API. Here’s a breakdown:

## 1. Downloading the Iris Dataset
The dataset is fetched using the `fetch_data` function from `utils.py`, which pulls data from a URL into a pandas DataFrame.

## 2. Data Transformation
The dataset is analyzed using Python’s SweetViz package, which generates an HTML report showing distributions, data types, and potential outliers. Boxplots were then used to visually identify outliers, which were found in the `sepal_width` feature. Four rows containing these outliers were removed from the dataset using the `remove_outliers` function.

## 3. Storing the Data
Rather than storing the cleaned data in a database like Postgres or AWS, it's saved as a Parquet file. Given the small size of the dataset and the relatively simple transformations applied to it, there’s no need to use a heavy database for storage. Parquet is a great choice here because it’s compact, fast to read, and simple to use for storing the cleaned data. You’ll find this file in the `data` folder under the name `iris_data_clean.parquet`.

## 4. Web API
A simple Flask-based web API is built to serve the Iris dataset and provide statistical summaries and visualizations. The API lets you easily interact with the data by accessing:
- **The full dataset**
- **Summary statistics**
- **Species-specific summary statistics**
- **Feature pairwise visualizations an feature distributions by species**
- **Top entries by smallest `sepal_width` and largest `petal_area`**

### How the App Works:
- **`main.py`**: This is the starting point of the app. Running this file first prepares the dataset (fetches, cleans, and stores it), then asks if you want to run the web API (`api.py`). If you choose to run the API, it starts in a separate thread and opens in your browser. You can skip the API part if you don’t need it.
- **`prep.py`**: This script handles fetching, cleaning, and saving the dataset. It’s responsible for removing outliers and storing the cleaned data as a Parquet file.
- **`api.py`**: This file sets up the Flask API. It loads the cleaned dataset and exposes various endpoints for you to interact with the data, including viewing summaries and generating visualizations. While in a production enviroment, it’s a good idea to restructure the application to separate the routing logic into distinct modules, this structure works just fine for the current scale.

### Other Key Files:
- **`utils.py`**: Contains helper functions like `fetch_data` (to download the dataset) and `remove_outliers` (to clean the data).
- **`data/iris_data_clean.parquet`**: The cleaned dataset stored as a Parquet file. 
- **`tests/test_api.py`**: Includes unit tests to ensure the API's endpoints work as expected. All tests passed successfully.

## How to Run with Dockerfile
   ```bash
   docker build -t mycontainer .

   docker run -p 5000:5000 mycontainer
```

After running the container, the API will be accessible at http://127.0.0.1:5000 or http://localhost:5000 in your web browser.

## How to Run without Dockerfile
   ```bash
   python app/main.py    
```

This version will produce some data visualisations about Iris dataset. API will be accessible at http://127.0.0.1:5000.