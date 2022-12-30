import customtkinter as ctk

import glob_style


class Numpad(ctk.CTkToplevel):
    def __init__(self, input_field, input_type, info_message):
        super().__init__()
        self.geometry(glob_style.screen_resolution)
        self.attributes("-fullscreen", True)
        self.config(cursor=glob_style.cursor)

        self.input_field = input_field
        self.input_type = input_type
        self.info_message = info_message

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.info_message_label = ctk.CTkLabel(self, text=self.info_message, font=glob_style.menu_button_font)
        self.info_message_label.grid(row=0, column=0, columnspan=4, sticky="news", padx=5, pady=5)

        self.value_display = ctk.CTkEntry(self, font=ctk.CTkFont(size=25))
        self.value_display.grid(row=1, column=0, columnspan=4, sticky="news", padx=5, pady=5)
        self.value_display.insert(0, self.input_field.get())

        self.button_1 = ctk.CTkButton(self, text="1", command=lambda: self.add_digit(1),
                                      font=glob_style.menu_button_font)
        self.button_1.grid(row=2, column=0, sticky="news", padx=5, pady=5)

        self.button_2 = ctk.CTkButton(self, text="2", command=lambda: self.add_digit(2),
                                      font=glob_style.menu_button_font)
        self.button_2.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        self.button_3 = ctk.CTkButton(self, text="3", command=lambda: self.add_digit(3),
                                      font=glob_style.menu_button_font)
        self.button_3.grid(row=2, column=2, sticky="news", padx=5, pady=5)

        self.button_4 = ctk.CTkButton(self, text="4", command=lambda: self.add_digit(4),
                                      font=glob_style.menu_button_font)
        self.button_4.grid(row=3, column=0, sticky="news", padx=5, pady=5)

        self.button_5 = ctk.CTkButton(self, text="5", command=lambda: self.add_digit(5),
                                      font=glob_style.menu_button_font)
        self.button_5.grid(row=3, column=1, sticky="news", padx=5, pady=5)

        self.button_6 = ctk.CTkButton(self, text="6", command=lambda: self.add_digit(6),
                                      font=glob_style.menu_button_font)
        self.button_6.grid(row=3, column=2, sticky="news", padx=5, pady=5)

        self.button_7 = ctk.CTkButton(self, text="7", command=lambda: self.add_digit(7),
                                      font=glob_style.menu_button_font)
        self.button_7.grid(row=4, column=0, sticky="news", padx=5, pady=5)

        self.button_8 = ctk.CTkButton(self, text="8", command=lambda: self.add_digit(8),
                                      font=glob_style.menu_button_font)
        self.button_8.grid(row=4, column=1, sticky="news", padx=5, pady=5)

        self.button_9 = ctk.CTkButton(self, text="9", command=lambda: self.add_digit(9),
                                      font=glob_style.menu_button_font)
        self.button_9.grid(row=4, column=2, sticky="news", padx=5, pady=5)

        self.button_0 = ctk.CTkButton(self, text="0", command=lambda: self.add_digit(0),
                                      font=glob_style.menu_button_font)
        self.button_0.grid(row=5, column=0, columnspan=2, sticky="news", padx=5, pady=5)

        if self.input_type == "float":
            self.button_comma = ctk.CTkButton(self, text=",", command=lambda: self.add_digit(","),
                                              font=glob_style.menu_button_font)
            self.button_comma.grid(row=5, column=2, sticky="news", padx=5, pady=5)
        elif self.input_type == "time":
            self.button_colon = ctk.CTkButton(self, text=":", command=lambda: self.add_digit(":"),
                                              font=glob_style.menu_button_font)
            self.button_colon.grid(row=5, column=2, sticky="news", padx=5, pady=5)

        self.button_delete = ctk.CTkButton(self, text="\u2190", command=self.remove_digit,
                                           font=glob_style.menu_button_font)
        self.button_delete.grid(row=2, column=3, rowspan=2, sticky="news", padx=5, pady=5)

        self.button_enter = ctk.CTkButton(self, text="ENTER", command=self.enter, font=glob_style.menu_button_font)
        self.button_enter.grid(row=4, column=3, rowspan=2, sticky="news", padx=5, pady=5)

    def add_digit(self, value):
        current_input = self.value_display.get()
        if not (value == ":" and current_input.count(":")) and not (value == "," and current_input.count(",")):
            self.value_display.insert(ctk.END, value)

    def remove_digit(self):
        current_input = self.value_display.get()
        if len(current_input) > 0:
            self.value_display.delete((len(current_input) - 1), ctk.END)

    def enter(self):
        self.input_field.delete(0, ctk.END)
        self.input_field.insert(0, self.value_display.get())
        self.withdraw()


class InfoMessage(ctk.CTkToplevel):
    def __init__(self, title="Info", message=""):
        super().__init__()
        self.message = message
        self.title = title

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.message_label = ctk.CTkLabel(self, text=self.message, font=glob_style.menu_button_font)
        self.message_label.grid(row=0, column=0, sticky="news", padx=7, pady=7)

        self.withdraw_button = ctk.CTkButton(self, text="OK", font=glob_style.menu_button_font, command=self.withdraw)
        self.withdraw_button.grid(row=1, column=0, sticky="news", padx=7, pady=7)
