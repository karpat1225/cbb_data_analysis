from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd 
import numpy as np
import zipfile


#Gather Data from kaggle API
api = KaggleApi()
api.authenticate()  
api.dataset_download_file(
    dataset="andrewsundberg/college-basketball-dataset",
    file_name="cbb25.csv",
    path="data/",
    quiet=False
)


df = pd.read_csv('data/cbb25.csv', na_values=['Not Available','unknown'])

print(df.head)
print(df.columns)