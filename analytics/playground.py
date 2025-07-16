import pandas as pd; import numpy as np

#%%
import os
BHAVDIR = '~/source/nse-data/data_files/BHAVCOPY'
data = pd.DataFrame()
bhav_file = 'bhavcopy_14-Jul-2025.csv'
try:
    data = pd.read_csv(os.path.join(BHAVDIR, bhav_file))
except FileNotFoundError:
    print(f"The File [{bhav_file}]is not found!")
print(f"Total Data size: [{len(data)}]")
