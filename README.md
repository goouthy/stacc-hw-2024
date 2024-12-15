# stacc-hw-2024
Homework for STACC Data Engineer position. Date: 15/12/2024.

The task involves handling, analysing, and storing the famous Iris dataset. Task is divided into following subtasks:

1. Downloading the Iris dataset

Used a function named "fetch_data" in utils.py. This function fetches a dataset given an URL, output path, and final dataset name into parquet file.

2. Performing simple transformations to the data

Firstly, analysed the dataset with Python's SweetViz package, which creates an html report for a given dataset, which helps to understand fast the data types, distributions and gives insight into potential outliers. Then proceded to dive deeper into potential outliers by creating boxplot charts for every feature in the dataset, which allowed me to see that the feature "sepal_width" had some outliers out of the interquantile range. Finally, removed these outliers (total of 4 rows) from the dataset.

For extra analysis, observed the pairwise relationships between features with scatterplots by species. This visualization helped clarify the differences between the different species. For example, clearly the three are different species as they form into three clusters. Most different of the species is the setosa species, whcih having the most distinct values, especially looking at petal length and width.

3. Storing the data

Although the point of this step probably was to see what technical skills I posses, I will rather demonstrate my understandmant of business optimisation, and will not use any tools which are not necessary for given task. Since the dataset is so small, and I don't see the need of querying the dataset using SQL nor do I have any need to further expand this project in the future, I will opt for saving the dataset as parquet. Parquet is simple to use, and will be compressed down even further, which makes it better than csv.

