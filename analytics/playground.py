import pandas as pd; import numpy as np

#%%
import os
BHAVDIR = '/home/akasmajhi/source/nse-data/data_files/BHAVCOPY'
data = pd.DataFrame()
bhav_file = 'bhavcopy_18-Jul-2025.csv'
try:
    file_to_read = os.path.join(BHAVDIR, bhav_file)
    print(f"File to Read: {file_to_read}")
    data = pd.read_csv(file_to_read)
except FileNotFoundError:
    print(f"The File [{bhav_file}]is not found!")
print(f"Total Data size: [{len(data)}]")

data.columns
data.index
# data[data.TckrSymb == 'INFY'].OpnPric
# data_ohlc = ""
only_infy = data.loc[data.TckrSymb == 'INFY']
only_infy[["TckrSymb", "OpnPric", "HghPric", "LwPric", "ClsPric", "PrvsClsgPric"]]
