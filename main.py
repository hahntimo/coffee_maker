import customtkinter as ctk
import multiprocessing

from GUI import analyse_menu
from controllers import motors
import glob_var
import glob_style

ctk.set_appearance_mode(glob_style.appearance_mode)
ctk.set_default_color_theme(glob_style.color_theme)


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
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
        glob_var.brewing_menu_frame = BrewingMenu()
        self.withdraw()

    def start_profile_menu(self):
        glob_var.profile_menu_frame = ProfileMenu()
        self.withdraw()

    def start_analysis_menu(self):
        glob_var.analysis_menu_frame = analyse_menu.AnalysisMenu()
        self.withdraw()


class BrewingMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes('-fullscreen', True)
        self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure(0, weight=1)

        self.menu_label = ctk.CTkLabel(self, text="Brühen", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)


class ProfileMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes('-fullscreen', True)

        self.grid_columnconfigure(0, weight=1)

        self.menu_label = ctk.CTkLabel(self, text="Brühprofile", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)


def run():
    # glob_var.pitcher_spinner_controller = motors.PitcherSpinnerController()
    # glob_var.pitcher_spinner_controller.start_thread()

    glob_var.pitcher_spinner_queue = multiprocessing.JoinableQueue()
    glob_var.pitcher_spinner_process = motors.PitcherSpinController(glob_var.pitcher_spinner_queue)
    glob_var.pitcher_spinner_process.start()

    glob_var.main_menu_frame = MainMenu()
    glob_var.main_menu_frame.mainloop()
    exit()


if __name__ == "__main__":
    run()
