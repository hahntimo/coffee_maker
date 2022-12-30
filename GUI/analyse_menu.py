import customtkinter as ctk
from tkinter import messagebox
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath("__main__")))
import glob_var
import glob_style
from GUI import helper


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
        # self.withdraw()

    def start_pitcher_spinner_menu(self):
        glob_var.analyse_pitcher_spinner_frame = PitcherSpinnerMenu()
        # self.withdraw()

    def start_heating_element_menu(self):
        glob_var.analyse_heating_element_frame = HeatingElementMenu()
        # self.withdraw()

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
        glob_var.pitcher_spinner_input_queue.put(("shutdown", None))
        for _ in range(10):
            try:
                os._exit(_)
            except:
                print("master kill fail", _)


class PumpMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.pump_volume_label_text = ctk.StringVar(self, "STOP")
        self.milliliters_per_minute = ctk.IntVar(self, 0)
        self.pumping_bool = False

        self.menu_label = ctk.CTkLabel(self, text="Pumpe", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, columnspan=2, padx=5, pady=15)

        self.volume_label = ctk.CTkLabel(self, text="Volumen in ml:", font=glob_style.menu_button_font)
        self.volume_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)
        self.volume_input = ctk.CTkEntry(self, font=glob_style.menu_button_font)
        self.volume_input.grid(row=1, column=1, sticky="news", padx=7, pady=7)
        self.volume_input.bind("<Button-1>", lambda _: helper.Numpad(input_field=self.volume_input,
                                                                     input_type="float",
                                                                     info_message="Pumpvolumen in ml:"))

        self.time_label = ctk.CTkLabel(self, text="Minuten:", font=glob_style.menu_button_font)
        self.time_label.grid(row=2, column=0, sticky="news", padx=7, pady=7)
        self.time_input = ctk.CTkEntry(self, font=glob_style.menu_button_font)
        self.time_input.grid(row=2, column=1, sticky="news", padx=7, pady=7)
        self.time_input.bind("<Button-1>", lambda _: helper.Numpad(input_field=self.time_input,
                                                                   input_type="time",
                                                                   info_message="Pumpzeit in Minuten:"))

        self.start_stop_button = ctk.CTkButton(self, text="Start", font=glob_style.menu_button_font,
                                               command=self.start_stop_pump)
        self.start_stop_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=7, pady=7)

        self.calibration_button = ctk.CTkButton(self, text="kalibrieren", font=glob_style.menu_button_font)
        self.calibration_button.grid(row=4, column=0, sticky="news", padx=7, pady=7)

        self.set_flowrate_button = ctk.CTkButton(self, text="Flussrate justieren", font=glob_style.menu_button_font,
                                                 command=self.set_flowrate)
        self.set_flowrate_button.grid(row=4, column=1, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=5, column=0, columnspan=2, sticky="wes", padx=7, pady=7)

    def return_menu(self):
        glob_var.analysis_menu_frame.deiconify()
        self.withdraw()

    def set_flowrate(self):
        helper.InfoMessage(title="Flussrate justieren", message="Bitte messbecher unterstellen")
        print("DONE")

    def start_stop_pump(self):
        if self.pumping_bool:
            self.start_stop_button.configure(text="start")
            glob_var.pump_process_input_queue.put("stop", None, None)
            self.pumping_bool = False

        else:
            if self.volume_input.get() == "":
                helper.InfoMessage(message="Fehlende Angabe: Pumpvolumen")
            elif self.time_input.get() == "":
                helper.InfoMessage(message="Fehlende Angabe: Pumpzeit")
            else:
                self.start_stop_button.configure(text="stop")
                time_input = self.time_input.get().split(":")
                if len(time_input) == 2:
                    time_in_seconds = (int(time_input[0]) if time_input[0] != "" else 0) * 60 + \
                                      (int(time_input[1]) if time_input[1] != "" else 0)
                else:
                    time_in_seconds = (int(time_input[0]) if time_input[0] != "" else 0) * 60

                volume_in_ml = float(self.volume_input.get().replace(",", "."))
                glob_var.pump_process_input_queue.put(("pump_task", volume_in_ml, time_in_seconds))
                self.pumping_bool = True


class PitcherSpinnerMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)

        self.revolution_label_text = ctk.StringVar(self, "STOP")
        self.revolution_u_min = ctk.IntVar(self, 0)

        self.menu_label = ctk.CTkLabel(self, text="Drehteller", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)

        self.revolution_label = ctk.CTkLabel(self, textvariable=self.revolution_label_text, font=ctk.CTkFont(size=40))
        self.revolution_label.grid(row=1, column=0, sticky="news", padx=7, pady=7)

        self.revolution_slider = ctk.CTkSlider(self, from_=-40, to=40, number_of_steps=80,
                                               variable=self.revolution_u_min, command=self.change_revolution)
        self.revolution_slider.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.calibration_button = ctk.CTkButton(self, text="kalibrieren", font=glob_style.menu_button_font,
                                                command=self.calibrate)
        self.calibration_button.grid(row=3, column=0, sticky="news", padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=4, column=0, sticky="wes", padx=7, pady=7)

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
        glob_var.pitcher_spinner_input_queue.put(("change_parameters", revolution))

    def calibrate(self):
        self.calibration_button.configure(text="Kalibrierung läuft...")
        time.sleep(0.5)
        glob_var.pitcher_spinner_input_queue.put(("calibrate", None))
        while True:
            time.sleep(0.1)
            return_type, data = glob_var.pitcher_spinner_output_queue.get()
            if return_type == "calibration_done":
                helper.InfoMessage(title="Kalibrierung", message=f"Delay: {data}")
                break
        self.calibration_button.configure(text="kalibrieren")


class HeatingElementMenu(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)

        self.heating_up_bool = False

        self.temperature_set_label_text = ctk.StringVar(self, "Zieltemperatur: 22 °C")
        self.temperature_actual_label_text = ctk.StringVar(self, "Wassertemperatur: ---")
        self.temperature_set = ctk.IntVar(self, 23)

        self.menu_label = ctk.CTkLabel(self, text="Heizelement", font=ctk.CTkFont(size=25))
        self.menu_label.grid(row=0, column=0, padx=5, pady=15)

        self.temperature_set_label = ctk.CTkLabel(self, textvariable=self.temperature_set_label_text,
                                                  font=ctk.CTkFont(size=40))
        self.temperature_set_label.grid(row=1, column=0, padx=7, pady=7)

        self.temperature_slider = ctk.CTkSlider(self, from_=23, to=99, number_of_steps=76, variable=self.temperature_set,
                                                command=self.change_temperature)
        self.temperature_slider.grid(row=2, column=0, sticky="news", padx=7, pady=7)

        self.temperature_actual_label = ctk.CTkLabel(self, textvariable=self.temperature_actual_label_text,
                                                     font=ctk.CTkFont(size=40))
        self.temperature_actual_label.grid(row=3, column=0, padx=7, pady=7)

        self.start_stop_button = ctk.CTkButton(self, text="Start", font=glob_style.menu_button_font,
                                               command=self.start_stop_heating)
        self.start_stop_button.grid(row=4, column=0, padx=7, pady=7)

        self.return_menu_button = ctk.CTkButton(self, text="\u21E6", font=glob_style.menu_button_font,
                                                command=self.return_menu, height=40)
        self.return_menu_button.grid(row=5, column=0, sticky="wes", padx=7, pady=7)

    def change_temperature(self, *args):
        temperature = self.temperature_set.get()
        self.temperature_set_label_text.set(f"Zieltemperatur: {temperature} °C")

    def start_stop_heating(self):
        if self.heating_up_bool:
            self.start_stop_button.configure(text="start")
            self.heating_up_bool = False
        else:
            self.start_stop_button.configure(text="stop")
            self.heating_up_bool = True

    def return_menu(self):
        glob_var.analysis_menu_frame.deiconify()
        self.withdraw()