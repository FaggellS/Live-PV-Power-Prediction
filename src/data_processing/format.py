import pandas as pd

dow_dict = {
    0:2, # monday
    1:3,
    2:4,
    3:5,
    4:6,
    5:7,
    6:1 # sunday


}


def format_for_storage(df):

    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")
    df = df.set_index("timestamp")

    df["pred_power"] = -1
    df["pred_time"] = -1
    df["rmse"] = -1
    df["state"] = "raw"

    return df


def format_for_model(df):

    out = []

    for _, row in df.iterrows():

        timestamp = row.name
        dow = day_of_week(timestamp)

        entry = [row["irradiance"], row["temperature"], row["true_power"], timestamp.hour, dow, timestamp.month]

        out.append(entry)

    return out

def prepare_input(k_last):


    return df_to_dict(k_last)


def df_to_dict(df):

    list_of_dict = []

    for _, row in df.iterrows():

        list_of_dict.append(
            {
                "timestamp": row.name,
                "irradiance": row["irradiance"],
                "temperature": row["temperature"],
                "true_power": row["true_power"]
            }
        )

    return list_of_dict
    


def day_of_week(timestamp):

    dow_datetime = timestamp.weekday()

    return dow_dict[dow_datetime]