# Step 1: Import required Libraries
print("Importing required libraries")
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import mltable
from create_client import ml_client
print("Libraries imported")

sns.set(style="whitegrid")

# Step 2: Load the raw dataset
dataset_name="raw_house_data"
print("Loading raw dataset")
data_asset = ml_client.data.get(f"{dataset_name}", version="1")
tbl = mltable.load(data_asset.path)
df = tbl.to_pandas_dataframe()
print("Dataset loaded")

print ("Describing dataset")
print(df.describe())

print("Showing dataset shape") # i.e number of rows and columns
print(df.shape)
print("Previewing dataset")
print(df.head(10))

# Understand the datastructure - schema, datatypes and null values
print("\n Datatypes and null values check")
print(df.info())

print("\n? Any missing values?")
print(df.isnull().sum())

# Step 3
# In this step, we clean and filter the dataset to ensure it only contained valid and relevant records.
# First, we removed any rows with missing values across columns to avoid issues caused by incomplete data.
# Next, we applied a filter to keep only entries where the property price was greater than 10,000, ensuring
# that extremely low or invalid prices were excluded. Finally, we restricted the dataset further by selecting
# only properties with more than 2,000 square feet, focusing the analysis on larger homes. This combination of
# cleaning and filtering produced a dataset that is both consistent and tailored to our analysis needs.

#Removes any rows in df that contain NaN (null / missing) values in any column.
# After this, every row left has complete data.
df = df.dropna()
#Applies a condition on the price column.
#Keeps only rows where the price is greater than 10,000.
#All rows with lower or missing prices are filtered out.
df = df[df['price'] > 10000]
#Applies another condition, this time on the sqft (square footage) column.
#Keeps only rows where sqft is greater than 2,000.
#Filters out smaller properties.
df = df[df['sqft'] > 2000]

print(df.head(100))