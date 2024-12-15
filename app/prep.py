import sweetviz as sv
import matplotlib.pyplot as plt
import seaborn as sns

from utils import fetch_data, remove_outliers

# STEP 1. Import Iris dataset
iris_data = fetch_data(
    "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
)

# STEP 2. Data analytics
print(f"Original shape of Iris dataset: {iris_data.shape}")

# SweetViz report to familiarize with the distributions of features
report = sv.analyze(iris_data)
report.show_html("iris_report.html")

# Identifying outliers
sns.boxplot(data=iris_data)
plt.title("Identifying outliers in Iris dataset features")
plt.show()

iris_data_no_outliers = remove_outliers(iris_data)

print(f"Shape of Iris dataset after outlier removal: {iris_data_no_outliers.shape}")

# STEP 3. Store transformed data
iris_data_no_outliers.to_parquet("data/iris_data_clean.parquet", engine="pyarrow")
