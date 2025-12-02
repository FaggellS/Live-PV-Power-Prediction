from gui.ui_definition import layout, ui_model_input, ui_simulator_params, ui_model_output, ui_misc


from gui import update_manager
from threading import Thread, Event
from typing import Optional


"""
gui_manager.py


"""


class GUI:

    def __init__(self, simulator):

        print("Initialize GUI...")

        self.thread: Optional[Thread] = None

        self.interval_values = [10, 5, 1, 0.5, 0.1, 0.05]
        self.sliding_values = [2,3,4,5]
        self.ahead_values = [10, 20, 40, 60]

        
        self.simulator = simulator
        self.simulator.set_callback(self.gui_update)


        self.root = layout.build_root()

        self.build_layout()
        self.build_ui()


    ## CREATE THE TKINTER WINDOW

    def run(self):
        self.root.mainloop()


    ## BUTTONS BEHAVIOR

    def startButtonPressed(self):
        print("start button pressed")

        if not self.thread or not self.thread.is_alive():
            try:
                self.simulator.stop_event.clear()
            except Exception:
                pass

        is_demo_mode = False
        
        if self.demo_mode.get() == 1:
            is_demo_mode = True



        param1 = float(self.param_box1.get().split(" ")[1]) # "Every X minute(s)"
        param2 = int(self.param_box2.get().split(" ")[0]) # "Y last recorded values"
        param3 = int(self.param_box3.get().split(" ")[0]) # "Z minutes ahead"

        self.thread = Thread(
            target = self.simulator.run,
            args = (is_demo_mode, param1, param2, param3, ),
            daemon = True
        )

        update_manager.handle_start_simulation(self, self.simulator, param1, param2)


        self.thread.start()

        

        # set status to ON

    def stopButtonPressed(self):
        print("stop button pressed")

        try:
            self.simulator.stop()
        except Exception:
            pass

        update_manager.handle_stop_simulation(self)


    ## SIMULATOR CALLS BACK FOR GUI UPDATE

    def gui_update(self, output_dict):

        update_manager.handle_update(self, self.simulator, output_dict)


    ## BUILDING LAYOUT

    def build_ui(self):
                

        self.demo_mode, self.param_box1, self.param_box2, self.param_box3, self.param_lb1, self.param_lb2, self.param_lb3 = ui_simulator_params.define_parameter_frame(self.parameter_frame, self.interval_values, self.sliding_values, self.ahead_values)

        self.button_frame, self.start_button, self.stop_button = ui_simulator_params.define_buttons(self.button_frame, self.startButtonPressed, self.stopButtonPressed)

        self.input_frame, self.input_table, self.input_table_labels = ui_model_input.define_input_frame(self.input_frame)

        # when receive update => self.input_grid = ui_model_input.adapt_rows(self.input_grid)

        self.output_frame, self.output_grid, self.output_table_labels = ui_model_output.define_output_frame(self.output_frame)

        self.status, self.start_time, self.finish_time, self.rmse_label = ui_misc.define_misc(self.top_bar, self.bottom_bar)





    def build_layout(self):

        ## layout of the root

        self.top_bar, self.main_frame, self.bottom_bar = layout.build_root_layout(self.root)

        ## layout of the main, center frame

        self.left_frame, self.right_frame = layout.main_frame_layout(self.main_frame)

        ## layout of the right side frame

        self.right_frame, self.input_frame, self.output_frame = layout.right_frame_layout(self.right_frame)

        self.parameter_frame, self.button_frame = layout.left_frame_layout(self.left_frame)

