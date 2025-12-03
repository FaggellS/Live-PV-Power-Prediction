from gui.ui_definition.ui_model_input import initialize_input_labels, update_input_labels
from gui.ui_definition.ui_model_output import initialize_output_labels, update_output_labels
from gui.ui_definition.ui_misc import update_time, update_status, update_rmse, start_timer

from datetime import datetime, timedelta

def handle_update(gui_manager, simulator, output_dict):

    if output_dict["time_end"] is None:

        handle_stop_simulation(gui_manager)

        return

    if output_dict["output_data"] is None:

        gui_manager.start_time, gui_manager.finish_time = update_time(gui_manager.start_time, gui_manager.finish_time, output_dict["time_start"], output_dict["time_end"])
        gui_manager.middle_label = update_rmse(gui_manager.middle_label, output_dict["interval"])
        
        gui_manager.input_table_labels = update_input_labels( gui_manager.input_table_labels, output_dict["input_data"])

    else:
        gui_manager.output_table_labels = update_output_labels( gui_manager.output_table_labels, output_dict["output_data"] )
        start_timer(gui_manager.root, gui_manager.middle_label, output_dict["interval"])






def handle_start_simulation(gui_manager, simulator, interval, sliding_window):

    gui_manager.status = update_status(gui_manager.status, True)
    
    gui_manager.input_table, gui_manager.input_table_labels = initialize_input_labels ( gui_manager.input_table, gui_manager.input_table_labels, sliding_window )
    gui_manager.output_table, gui_manager.output_table_labels = initialize_output_labels ( gui_manager.output_grid, gui_manager.output_table_labels )


def handle_stop_simulation(gui_manager):

    gui_manager.status = update_status(gui_manager.status, False)
    gui_manager.start_time, gui_manager.finish_time = update_time(gui_manager.start_time, gui_manager.finish_time, "--", "--")