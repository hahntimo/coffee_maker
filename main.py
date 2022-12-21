import customtkinter as ctk

from GUI import analyse_menu
import glob_var
import glob_style

ctk.set_appearance_mode(glob_style.appearance_mode)
ctk.set_default_color_theme(glob_style.color_theme)


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes('-fullscreen', True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.button_font = ctk.CTkFont(size=30, weight="bold")

        self.version_label = ctk.CTkLabel(self, text=f"Version: {glob_var.__version__}")
        self.version_label.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        self.start_brew_menu_button = ctk.CTkButton(self, text="Brühen", font=self.button_font,
                                                    command=self.start_brew_menu)
        self.start_brew_menu_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.profile_menu_button = ctk.CTkButton(self, text="Profile", font=self.button_font,
                                                 command=self.start_profile_menu)
        self.profile_menu_button.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.analysis_menu_button = ctk.CTkButton(self, text="Analyse", font=self.button_font,
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


if __name__ == "__main__":
    glob_var.main_menu_frame = MainMenu()
    glob_var.main_menu_frame.mainloop()
    exit()
