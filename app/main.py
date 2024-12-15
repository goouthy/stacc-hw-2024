from flask import Flask, request, jsonify
import pandas as pd
import sweetviz as sv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils import fetch_data, detect_outliers, remove_outliers

### STEP 1. Import Iris dataset

# url = "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"

# # Saving to data directory under name iris.csv
# fetch_data(url, "data", "iris")


### STEP 2. Data analytics

# Data under analysis
# iris_data = pd.read_csv("data/iris.csv")

# print(f"Original shape of Iris dataset: {iris_data.shape}")

# # SweetViz report to familirize with the distributions of features
# report = sv.analyze(iris_data)
# report.show_html("iris_report.html")

# # Identifying outliers
# sns.boxplot(data=iris_data)
# plt.title('Identifying outliers in Iris dataset features')
# plt.show()

# # Feature "sepal_width" shows outliers out of the interquantile range when observed the boxplots. Removing those rows.

# iris_data_no_outliers = remove_outliers(iris_data)

# print(f"Shape of Iris dataset after outlier removal: {iris_data_no_outliers.shape}")

# # Now visualizing pairwise relationships between features with scatterplots by species
# sns.pairplot(iris_data_no_outliers, hue="species")
# plt.show()

# Seeing clear patterns for each species with setosa (blue) having the most distinct values, especially looking at petal length and width.
# It is clear to see that these are three separate species by observed features.


### STEP 3. Store transformed data

# The dataset is so small and since I don't see future need to either SQL query it, or no other data to add to the project, so
# I will save it to parquet, rather than any SQL assistant or AWS

# iris_data_no_outliers.to_parquet('data/iris_data_clean.parquet', engine='pyarrow')


### STEP 4

import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask, request, render_template_string
import pandas as pd
import os
import numpy as np

app = Flask(__name__)

# Define the path to the Parquet file
file_path = 'data/iris_data_clean.parquet'

os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Load the data from Parquet
df = pd.read_parquet(file_path, engine='pyarrow')

# Global CSS Styles to be applied across all templates
CSS_STYLES = '''
<style>
    body {
        font-family: 'Helvetica', sans-serif;
        background-color: #f4f4f9;
        text-align: left;
    }
    h1, h2 {
        color: #4CAF50;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    li {
        font-size: 18px;
        margin-bottom: 10px;
    }
    a {
        text-decoration: none;
        color: #4CAF50;
        font-weight: bold;
    }
    a:hover {
        color: #333;
    }
    table {
        width: 90%;
        margin: 20px auto;
        border-collapse: collapse;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    th, td {
        padding: 10px;
        text-align: center;
        border: 1px solid #ddd;
    }
    th {
        background-color: #4CAF50;
        color: white;
        text-transform: uppercase;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tr:hover {
        background-color: #e1f1e1;
    }
</style>
'''

# Root route
@app.route('/')
def home():
    return render_template_string(CSS_STYLES + """
        <h1>Welcome to the Iris Dataset API!</h1>
        <p>Here are the available endpoints:</p>
        <ul>
            <li><b><a href="/data">/data</a></b> - See the whole dataset</li>
            <li><b><a href="/full_summary">/full_summary</a></b> - See summary statistics for the whole dataset</li>
            <li><b><a href="/species_summary">/species_summary</a></b> - See summary statistics grouped by species</li>
            <li><b><a href="/pairplot">/pairplot</a></b> - View a pairplot visualization of relationships between features and feature distributions by species</li>
            <li><b><a href="/top_n?n=5&column=sepal_width">/top_n</a></b> - See top 5 entries with smallest sepal widths</li>
            <li><b><a href="/largest_petal">/largest_petal</a></b> - See the largest petal surface area per species</li>
        </ul>
    """)

# Fetch all data
@app.route('/data', methods=['GET'])
def get_data():
    result = df.copy()
    result.reset_index(drop=True, inplace=True)
    result.index += 1
    result = result[['species'] + [col for col in result.columns if col != 'species']]
    result_html = result.to_html(classes='table table-striped')
    return render_template_string(CSS_STYLES + """
        <h2>All Data</h2>
        <p>Here is the full Iris dataset:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ result_html|safe }}
        </div>
    """, result_html=result_html)

# Full summary statistics 
@app.route('/full_summary', methods=['GET'])
def get_full_summary():
    summary = df.describe().loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    summary_transposed = summary.T
    summary_transposed = summary_transposed.drop(columns='petal_area', errors='ignore')
    summary_html = summary_transposed.to_html(classes='table table-striped')
    return render_template_string(CSS_STYLES + """
        <h2>Full Summary Statistics</h2>
        <p>This table shows summary statistics (mean, std, min, max, percentiles) for numeric columns in the Iris dataset:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ summary_html|safe }}
        </div>
    """, summary_html=summary_html)

# Species summary statistics
@app.route('/species_summary', methods=['GET'])
def get_species_summary():
    try:
        species_summary = df.groupby('species').describe().stack(level=0).reset_index()
        species_summary.columns = ['species', 'stat', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
        species_summary = species_summary[species_summary['stat'] != 'species']
        species_summary['count'] = species_summary['count'].astype(int)
        species_summary_html = species_summary.to_html(classes='table table-striped')
        return render_template_string(CSS_STYLES + """
            <h2>Species Summary Statistics</h2>
            <p>This table shows summary statistics grouped by species:</p>
            <div style="overflow-x:auto; text-align:center;">
                {{ species_summary_html|safe }}
            </div>
        """, species_summary_html=species_summary_html)
    except KeyError as e:
        return f"Error: {e}"

# Pairplot route (visualization)
@app.route('/pairplot', methods=['GET'])
def pairplot():
    sns.pairplot(df, hue="species")
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return render_template_string(CSS_STYLES + """
        <h2>Pairplot Visualization</h2>
        <p>This pairplot visualizes the relationships between different features of the Iris dataset, colored by species.</p>
        <img src="data:image/png;base64,{{ img_base64 }}" alt="Pairplot"/>
    """, img_base64=img_base64)

# Largest petal surface per species
@app.route('/largest_petal', methods=['GET'])
def largest_petal():
    df['petal_area'] = np.pi * df['petal_length'] * df['petal_width']
    largest_petal = df.loc[df.groupby('species')['petal_area'].idxmax()]
    largest_petal = largest_petal.round({'petal_area': 2})
    largest_petal_html = largest_petal[['petal_area', 'petal_length', 'petal_width', 'species']].to_html(classes='table table-striped')
    return render_template_string(CSS_STYLES + """
        <h2>Largest Petal Surface per Species</h2>
        <p>This table shows the instance with the largest petal surface area for each species:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ largest_petal_html|safe }}
        </div>
    """, largest_petal_html=largest_petal_html)

# Top N smallest sepal_width
@app.route('/top_n', methods=['GET'])
def top_n():
    n = request.args.get('n', default=5, type=int)
    top_n_sepal_width = df.nsmallest(n, 'sepal_width')

    columns = ['species'] + [col for col in top_n_sepal_width.columns if col != 'species']
    top_n_sepal_width = top_n_sepal_width[columns]

    top_n_html = top_n_sepal_width.to_html(classes='table table-striped', escape=False)
    top_n_html = top_n_html.replace('<th>sepal_width</th>', '<th style="font-weight: bold;">sepal_width</th>')

    for index, row in top_n_sepal_width.iterrows():
        top_n_html = top_n_html.replace(f'<td>{row["sepal_width"]}</td>',
                                        f'<td style="font-weight: bold;">{row["sepal_width"]}</td>')

    return render_template_string(CSS_STYLES + """
        <h2>Top {{n}} Smallest Sepal Width</h2>
        <p>This table shows the {{n}} flowers with the smallest sepal width:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ top_n_html|safe }}
        </div>
    """, top_n_html=top_n_html)

if __name__ == '__main__':
    app.run(debug=True)

