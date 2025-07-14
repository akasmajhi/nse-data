import pandas as pd; import numpy as np

#%%
import os
BHAVDIR = '~/source/nse-data/data_files/BHAVCOPY'
data = pd.read_csv(os.path.join(BHAVDIR, 'bhavcopy_11-Jul-2025.csv'))
print(f"Total Data size: [{len(data)}]")
