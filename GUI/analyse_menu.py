import customtkinter as ctk
import sys
import os
import RPi.GPIO as GPIO

sys.path.append(os.path.dirname(os.path.abspath("__main__")))
import glob_var
import glob_style


class AnalysisMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)

        self.fullscreen_bool = True

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.menu_label = ctk.CTkLabel(self, text="Analysemenü", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, columnspan=3, padx=5, pady=15)

        self.start_pump_menu_button = ctk.CTkButton(self, text="Pumpe", font=glob_style.menu_button_font,
                                                    command=self.start_pump_menu)
        self.start_pump_menu_button.grid(row=1, column=0, columnspan=3, sticky="news", padx=7, pady=7)

        self.start_pitcher_spinner_button = ctk.CTkButton(self, text="Drehteller", font=glob_style.menu_button_font,
                                                          command=self.start_pitcher_spinner_menu)
        self.start_pitcher_spinner_button.grid(row=2, column=0, columnspan=3, sticky="news", padx=7, pady=7)

        self.start_heater_menu_button = ctk.CTkButton(self, text="Heizelement", font=glob_style.menu_button_font,
                                                      command=self.start_heating_element_menu)
        self.start_heater_menu_button.grid(row=3, column=0, columnspan=3, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=4, column=0, sticky="we", padx=7, pady=7)

        self.minimize_maximize_button = ctk.CTkButton(self, text="minimireren", command=self.minimize_maximize,
                                                      height=40, font=ctk.CTkFont(size=20))
        self.minimize_maximize_button.grid(row=4, column=1, sticky="we", padx=7, pady=7)

        self.shutdown_button = ctk.CTkButton(self, text="schließen", command=self.shutdown_app, height=40,
                                             font=ctk.CTkFont(size=20))
        self.shutdown_button.grid(row=4, column=2, sticky="we", padx=7, pady=7)

    def start_pump_menu(self):
        glob_var.analyse_pump_frame = PumpMenu()
        self.withdraw()

    def start_pitcher_spinner_menu(self):
        glob_var.analyse_pitcher_spinner_frame = PitcherSpinnerMenu()
        self.withdraw()

    def start_heating_element_menu(self):
        glob_var.analyse_heating_element_frame = HeatingElementMenu()
        self.withdraw()

    def return_menu(self):
        glob_var.main_menu_frame.deiconify()
        self.withdraw()

    def minimize_maximize(self):
        if self.fullscreen_bool:
            self.fullscreen_bool = False
            self.minimize_maximize_button.configure(text="maximieren")
            self.attributes("-fullscreen", False)
            self.iconify()

        else:
            self.fullscreen_bool = True
            self.minimize_maximize_button.configure(text="minimieren")
            self.attributes("-fullscreen", True)

    def shutdown_app(self):
        glob_var.pitcher_spinner_queue.put(("shutdown", None))
        print("PROCESS KILLED")
        quit()
        print("test1")
        quit()
        print("test2")
        quit()
        print("test3")
        quit()


class PumpMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)


class PitcherSpinnerMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        # self.geometry(glob_style.screen_resolution)
        # self.attributes("-fullscreen", True)
        # self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.revolution_label_text = ctk.StringVar(self, "STOP")
        self.revolution_u_min = ctk.IntVar(self, 0)

        self.menu_label = ctk.CTkLabel(self, text="Drehteller", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)

        self.revolution_label = ctk.CTkLabel(self, textvariable=self.revolution_label_text, font=ctk.CTkFont(size=40))
        self.revolution_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.revolution_slider = ctk.CTkSlider(self, from_=-40, to=40, number_of_steps=40,
                                               variable=self.revolution_u_min, command=self.change_revolution)
        self.revolution_slider.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=4, column=0, sticky="we", padx=7, pady=7)

    def return_menu(self):
        glob_var.analysis_menu_frame.deiconify()
        self.withdraw()

    def change_revolution(self, *args):
        revolution = self.revolution_u_min.get()
        dir_substring = ""
        if revolution > 0:
            dir_substring = " rechts"
        elif revolution < 0:
            dir_substring = " links"
        label_text = f"Drehzahl: {abs(revolution)} U/min{dir_substring}"
        if revolution == 0:
            label_text = "STOP"

        self.revolution_label_text.set(label_text)
        glob_var.pitcher_spinner_queue.put(("change_parameters", revolution))


class HeatingElementMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()