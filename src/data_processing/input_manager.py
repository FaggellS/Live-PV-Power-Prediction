from data_processing.extract import extract_input_dfs, extract_last_input
from data_processing.synchronize import synchronize_dfs, merge_row
from data_processing.format import format_for_storage

from data_sources.hist_dataset import save_merged,remove_merged


from datetime import timedelta



class InputManager:

    def __init__(self):
        
        self.demo_mode = False


    def set_demo_mode(self, is_demo_mode):

        self.demo_mode = is_demo_mode



    def get_last_entry(self, timestamp):


        ts, irr_val, temp_val, power_val = extract_last_input(timestamp, self.demo_mode)

        as_df = merge_row(ts, irr_val, temp_val, power_val)

        return ts, format_for_storage(as_df)
    



    def load_current(self, timestamp):

        irr_df, temp_df, power_df = extract_input_dfs(self.demo_mode)



        df = synchronize_dfs(irr_df, temp_df, power_df)

        ## further preprocessing ? (nas, imputation,..)

        df = format_for_storage(df)

        if self.demo_mode:

            remove_merged()
            save_merged(df) # then when we retrieve the latest entry we will save time, altough in live mode we won't

            # restrict to current timestamp when saving to storage

            df = self.restrict_to_timestamp(df, timestamp)


        return df
    
    
    def restrict_to_timestamp(self, df, timestamp):

        
        
        return df[ df.index <= timestamp ] 