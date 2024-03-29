import multiprocessing

__version__ = "0.0.2"

# main menu
main_menu_frame = None
brewing_menu_frame = None
profile_menu_frame = None

# analysis menu
analysis_menu_frame = None
analyse_pitcher_spinner_frame = None
analyse_pump_frame = None
analyse_heating_element_frame = None
analyse_water_flow_frame = None

# controllers
pitcher_spinner_process = None
pitcher_spinner_input_queue = multiprocessing.Queue()
pitcher_spinner_output_queue = multiprocessing.Queue()

pump_process = None
pump_process_input_queue = multiprocessing.Queue()
pump_process_output_queue = multiprocessing.Queue()

heater_process = None
heater_process_input_queue = multiprocessing.Queue()
heater_process_output_queue = multiprocessing.Queue()

switch_process = None
switch_process_input_queue = multiprocessing.Queue()
switch_process_output_queue = multiprocessing.Queue()