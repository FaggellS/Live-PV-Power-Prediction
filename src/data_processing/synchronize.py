import pandas as pd

def merge_row(ts, irr_val, temp_val, power_val):

    as_df = pd.DataFrame(
        {
            "timestamp": [ts],
            "irradiance": [irr_val],
            "temperature": [temp_val],
            "true_power": [power_val]
        }
    )

    as_df.set_index("timestamp")

    return as_df

def synchronize_dfs(irr_df, temp_df, power_df):
    
    merged_df = merge_on_timestamp(irr_df, temp_df)
    merged_df = merge_on_timestamp(merged_df, power_df)


    return merged_df


def merge_on_timestamp(df1, df2):
    return pd.merge(df1, df2, on='timestamp', how='inner')