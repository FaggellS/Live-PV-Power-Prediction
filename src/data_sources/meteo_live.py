import requests
import pandas as pd
import io

# station_id = 7220

# API endpoint
BASE_URL = "https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/sio/ogd-smn_sio_t_now.csv"

# column names of interest, from meteoSwiss auto weather station
timestamp_col = "reference_timestamp"
radiation_col = "gre000z0" # "global radiation" 
temperature_col = "tresurs0" # "air temperature at surface"


def fetch_sion_weather(timestamp):
    """
    fetchs RADIATION and temperature from meteoSwiss
    """

    try:
        r = requests.get(BASE_URL, timeout=4)
        r.raise_for_status()
    except Exception as e:
        print("data_sources.meteo_live.py - MeteoSwiss API error:", e)
        return None, None


    raw = r.content.decode("utf-8")   # convert bytes → string

    df = pd.read_csv(io.StringIO(raw), sep=";", usecols=[timestamp_col, radiation_col, temperature_col])

    df = df.rename(columns={
        "reference_timestamp":"timestamp",
        "gre000z0": "radiation",
        "tresurs0": "temperature"
    })

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%d.%m.%Y %H:%M"
    )

    df = df.set_index("timestamp")

    return df #float(radiation), float(temperature)



def fetch_last(timestamp):

    df = fetch_sion_weather(timestamp)

    row = df.iloc[df.index.get_indexer([timestamp], method="nearest")]

    temperature = row[temperature_col].item()
    radiation = row[radiation_col].item()

    return float(radiation), float(temperature)