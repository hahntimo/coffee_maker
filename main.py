import sys

import customtkinter as ctk

import glob_style
import glob_var
from GUI import analyse_menu

ctk.set_appearance_mode(glob_style.appearance_mode)
ctk.set_default_color_theme(glob_style.color_theme)


class MainMenu(ctk.CTk):
    def __init__(self, dry_run):
        super().__init__()
        self.dry_run = dry_run
        self.geometry(glob_style.screen_resolution)
        if not self.dry_run:
            self.attributes('-fullscreen', True)
            self.config(cursor=glob_style.cursor)

        glob_style.menu_button_font = ctk.CTkFont(size=30, weight="bold")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.version_label = ctk.CTkLabel(self, text=f"Version: {glob_var.__version__}")
        self.version_label.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        self.start_brew_menu_button = ctk.CTkButton(self, text="Brühen", font=glob_style.menu_button_font,
                                                    command=self.start_brew_menu)
        self.start_brew_menu_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.profile_menu_button = ctk.CTkButton(self, text="Profile", font=glob_style.menu_button_font,
                                                 command=self.start_profile_menu)
        self.profile_menu_button.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.analysis_menu_button = ctk.CTkButton(self, text="Analyse", font=glob_style.menu_button_font,
                                                  command=self.start_analysis_menu)
        self.analysis_menu_button.grid(row=3, column=0, sticky="news", padx=7, pady=7)

    def start_brew_menu(self):
        glob_var.brewing_menu_frame = BrewingMenu(self.dry_run)
        # self.withdraw()

    def start_profile_menu(self):
        glob_var.profile_menu_frame = ProfileMenu(self.dry_run)
        # self.withdraw()

    def start_analysis_menu(self):
        glob_var.analysis_menu_frame = analyse_menu.AnalysisMenu(self.dry_run)
        # self.withdraw()


class SubMenu(ctk.CTkToplevel):
    def __init__(self, dry_run):
        super().__init__()
        self.dry_run = dry_run
        self.geometry(glob_style.screen_resolution)
        if not self.dry_run:
            self.attributes('-fullscreen', True)
            self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure(0, weight=1)
        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=5, column=0, sticky="wes", padx=7, pady=7)

    def return_menu(self):
        self.deiconify()
        self.withdraw()


class BrewingMenu(SubMenu):
    def __init__(self, dry_run):
        super().__init__(dry_run)
        self.menu_label = ctk.CTkLabel(self, text="Brühen", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)


class ProfileMenu(SubMenu):
    def __init__(self, dry_run):
        super().__init__(dry_run)
        self.menu_label = ctk.CTkLabel(self, text="Brühprofile", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)


def run(opts):
    operating_platform = sys.platform
    if operating_platform == "linux" and not opts.dry_run:
        from controllers import motors

        # pitcher spinner
        glob_var.pitcher_spinner_process = \
            motors.PitcherSpinController(task_queue=glob_var.pitcher_spinner_input_queue,
                                         output_queue=glob_var.pitcher_spinner_output_queue)
        glob_var.pitcher_spinner_process.start()

        # pump
        glob_var.pump_process = motors.PumpController(task_queue=glob_var.pump_process_input_queue,
                                                      output_queue=glob_var.pump_process_output_queue)
        glob_var.pump_process.start()

        # heater
        glob_var.heater_process = motors.Heater(task_queue=glob_var.heater_process_input_queue,
                                                output_queue=glob_var.heater_process_output_queue)
        glob_var.heater_process.start()

    else:
        print("OS:", operating_platform)

    glob_var.main_menu_frame = MainMenu(opts)
    glob_var.main_menu_frame.mainloop()
    quit()


def params():
    import argparse
    parser = argparse.ArgumentParser(description='Coffee Maker',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dry-run', action='store_true', help='Allow running without an RasPi.')
    return parser.parse_args()


if __name__ == "__main__":
    options = params()
    run(options)
