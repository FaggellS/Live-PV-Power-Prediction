from data_sources import meteo_live, pv_live, hist_dataset
import pandas as pd




def extract_last_input(timestamp, demo_mode):

    if demo_mode:

        ts, irr_val, temp_val, power_val = get_last_simulated(timestamp)
    
    else:

        ts, irr_val, temp_val, power_val = get_last_live(timestamp)
    

    return ts, irr_val, temp_val, power_val



def extract_input_dfs(demo_mode):

    if demo_mode:

        irr_df, temp_df, power_df = extract_simulated_data()

    else: 

        irr_df, temp_df, power_df = extract_live_data()

    return irr_df, temp_df, power_df



###





def extract_live_data():

    return None, None, None

    meteo_df = meteo_live.fetch_sion_weather()
    power_raw = pv_live.get()





def get_last_live(timestamp):

    return timestamp, None, None, None

    rad, temp = meteo_live.fetch_last(timestamp)

    pv = pv_live.get()

    return timestamp, rad, temp, pv



###





def extract_simulated_data():


    irr_df, temp_df, power_df = hist_dataset.get_separated()

    



    return irr_df, temp_df, power_df




def get_last_simulated(timestamp):

    df = hist_dataset.get_merged()

    if df is not None:

        row = df.iloc[df.index.get_indexer([timestamp], method="nearest")]

        print(f"HELLOOOOO : {row.index},\n{row.index[0]}")

        return row.index[0], row["irradiance"].item(), row["temperature"].item(), row["true_power"].item()

    else:

        irr_df, temp_df, power_df = extract_simulated_data()

        irr_row = irr_df[ irr_df["timestamp"] <= timestamp ].iloc[-1]
        temp_row = temp_df[ temp_df["timestamp"] <= timestamp ].iloc[-1]
        power_row = power_df[ power_df["timestamp"] <= timestamp ].iloc[-1]

        print(f"extract check: irr_id == others: {irr_row["timestamp"] == temp_row["timestamp"]}, {irr_row["timestamp"] == power_row["timestamp"]}")

        return irr_df["timestamp"], irr_row["irradiance"].item(), temp_row["temperature"].item(), power_row["true_power"].item()


###


