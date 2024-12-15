import os
from io import BytesIO
import base64

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from flask import Flask, render_template_string

# STEP 4. Write web API

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
            <li><b><a href="/dataset">All Data</a></b></li> 
            <li><b><a href="/summary">Full Summary Statistics</a></b></li> 
            <li><b><a href="/species_summary">Summary Statistics by Species</a></b></li> 
            <li><b><a href="/feature_pairplot">Pairplot Visualization</a></b></li> 
            <li><b><a href="/min_sepal_widths">Top Smallest Sepal Width</a></b></li> 
            <li><b><a href="/largest_petal_area">Largest Petal Surface per Species</a></b></li> 
        </ul>
    """)

# Fetch all data
@app.route('/dataset', methods=['GET'])
def get_data():
    result = df.copy()
    result.reset_index(drop=True, inplace=True)
    result.index += 1
    result = result[['species'] + [col for col in result.columns if col != 'species' and col != 'petal_area']]
    result_html = result.to_html(classes='table table-striped')
    return render_template_string(CSS_STYLES + """
        <h2>All Data</h2>
        <p>Here is the full Iris dataset:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ result_html|safe }}
        </div>
    """, result_html=result_html)

# Full summary statistics 
@app.route('/summary', methods=['GET'])
def get_full_summary():
    summary = df.describe().loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    summary_transposed = summary.T
    summary_transposed = summary_transposed.drop(columns=['petal_area'], errors='ignore')  # Remove 'petal_area'
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
            <h2>Summary Statistics by Species</h2>
            <p>This table shows summary statistics grouped by species:</p>
            <div style="overflow-x:auto; text-align:center;">
                {{ species_summary_html|safe }}
            </div>
        """, species_summary_html=species_summary_html)
    except KeyError as e:
        return f"Error: {e}"

# Pairplot route (visualization)
@app.route('/feature_pairplot', methods=['GET'])
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

# Top 5 smallest sepal_width
@app.route('/min_sepal_widths', methods=['GET'])
def top_n():
    n = 5  
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

# Largest petal surface per species
@app.route('/largest_petal_area', methods=['GET'])
def largest_petal():
    df['petal_area'] = np.pi * df['petal_length'] * df['petal_width']
    largest_petal = df.loc[df.groupby('species')['petal_area'].idxmax()]
    largest_petal = largest_petal.round({'petal_area': 2})
    
    largest_petal = largest_petal[['species', 'petal_area', 'petal_length', 'petal_width']]
    largest_petal = largest_petal.sort_values(by='petal_area', ascending=False)
    
    largest_petal_html = largest_petal.to_html(classes='table table-striped')
    return render_template_string(CSS_STYLES + """
        <h2>Largest Petal Surface per Species</h2>
        <p>This table shows the instance with the largest petal surface area for each species:</p>
        <div style="overflow-x:auto; text-align:center;">
            {{ largest_petal_html|safe }}
        </div>
    """, largest_petal_html=largest_petal_html)

if __name__ == "__main__":
    app.run(debug=False)
