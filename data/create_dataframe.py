import pandas, mltable
from create_connection import ml_client
from create_dataset import dataset_name
from create_connection import ml_client


data_asset = ml_client.data.get(dataset_name, version="1")
tbl = mltable.load(data_asset.path)
df = tbl.to_pandas_dataframe()
df

# Display the first 10 rows of the DataFrame to preview the data
print(df.head(10))
# Display summary statistics (count, mean, std, min, max, etc.) for numeric columns
print(df.describe())


