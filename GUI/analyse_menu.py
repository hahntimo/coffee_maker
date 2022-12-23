import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath("__main__")))
import glob_var
import glob_style


class AnalysisMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.fullscreen = True

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.button_font = ctk.CTkFont(size=30, weight="bold")

        self.menu_label = ctk.CTkLabel(self, text="Analysemenü", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, columnspan=2, padx=5, pady=15)

        self.start_pump_menu_button = ctk.CTkButton(self, text="Pumpe", font=self.button_font)
        self.start_pump_menu_button.grid(row=1, column=0, columnspan=2, sticky="news", padx=7, pady=7)

        self.start_pot_spinner_button = ctk.CTkButton(self, text="Drehteller", font=self.button_font)
        self.start_pot_spinner_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=7, pady=7)

        self.start_heater_menu_button = ctk.CTkButton(self, text="Heizelement", font=self.button_font)
        self.start_heater_menu_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=self.button_font, command=self.return_menu,
                                                height=40)
        self.return_menu_button.grid(row=4, column=0, sticky="we", padx=7, pady=7)

        self.minimize_maximize_button = ctk.CTkButton(self, text="minimireren", command=self.minimize_maximize,
                                                      height=40, font=ctk.CTkFont(size=20))
        self.minimize_maximize_button.grid(row=4, column=1, sticky="we", padx=7, pady=7)

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()

    def minimize_maximize(self):
        if self.fullscreen:
            self.fullscreen = False
            self.minimize_maximize_button.configure(text="maximieren")
            self.attributes("-fullscreen", False)
            self.iconify()

        else:
            self.fullscreen = True
            self.minimize_maximize_button.configure(text="minimieren")
            self.attributes("-fullscreen", True)


class PumpMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)


class CanSpinnerMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)