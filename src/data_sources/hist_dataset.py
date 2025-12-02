from os.path import dirname, join as pjoin
from os.path import exists
from os import remove
import pandas as pd

# cleaned, 10 min intervals
irr_dir = pjoin('..', 'data', 'raw', 'completed_dataset_irradiance.xlsx') 
temp_dir = pjoin('..', 'data', 'raw', 'completed_dataset_temperature.xlsx')
hist_out_dir = pjoin('..', 'data','raw', 'reduced_dataset_mean_PVpower.xlsx')

path_to_merged = pjoin('..', 'data', 'merged_simulated_data.xlsx')


def get_merged():

    if exists(path_to_merged):
        print(f"data_sources.hist_dataset - Retrieving existing merged dataset")
        df = pd.read_excel(path_to_merged)
        df = df.set_index("timestamp")
        return df
    else:
        return None


def save_merged(df):
    print(f"data_sources.hist_dataset - Saving merged dataset")

    df.to_excel(path_to_merged, index=True)

def remove_merged():

    if exists(path_to_merged):
        print(f"data_sources.hist_dataset - Removing merged dataset")
        remove(path_to_merged)
        return True
    
    return False

def get_separated():

    irr_df = pd.read_excel(irr_dir, header=0, names=["timestamp","irradiance"], usecols="A:B")
    temp_df = pd.read_excel(temp_dir, header=0, names=["timestamp","temperature"], usecols="A:B")
    power_df = pd.read_excel(hist_out_dir, header=0, names=["timestamp","true_power"], usecols="A:B")

    return irr_df, temp_df, power_df

