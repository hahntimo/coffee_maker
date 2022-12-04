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
        self.attributes('-fullscreen', True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.button_font = ctk.CTkFont(size=30, weight="bold")

        self.menu_label = ctk.CTkLabel(self, text="Analysemenü", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)

        self.start_pump_menu_button = ctk.CTkButton(self, text="Pumpe", font=self.button_font)
        self.start_pump_menu_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.start_pot_spinner_button = ctk.CTkButton(self, text="Kanne drehen", font=self.button_font)
        self.start_pot_spinner_button.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.start_heater_menu_button = ctk.CTkButton(self, text="Heizelement", font=self.button_font)
        self.start_heater_menu_button.grid(row=3, column=0, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=self.button_font, command=self.return_menu)
        self.return_menu_button.grid(row=4, column=0, sticky="we", padx=7, pady=7)

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()


class PumpMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes('-fullscreen', True)