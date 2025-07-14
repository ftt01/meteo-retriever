import pandas as pd
import numpy as np

def delete_negatives(path):
    data = pd.read_csv(path, index_col=0)
    data[data<0] = 0
    data.to_csv(path)

delete_negatives('/media/windows/projects/bias_correction/applications/era5land/data/30years/precipitation_kriging.csv')