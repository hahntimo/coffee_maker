import git
import os
import requests
import time
from traceback import format_exc
import customtkinter as ctk

import glob_style

ctk.set_appearance_mode(glob_style.appearance_mode)
ctk.set_default_color_theme(glob_style.color_theme)


class AutoDeployer:
    def __init__(self):
        self.branch = "main"
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.repo_path)
        self.repository = git.Repo(self.repo_path)

        self.loading_frame = None
        self.loading_screen_label = None

    def pull(self):
        for attempt in range(10):
            try:
                requests.head("https://google.com", timeout=1)
                self.repository.git.checkout(self.branch)
                current_repo_state = self.repository.head.commit
                self.repository.remotes.origin.pull()

                if current_repo_state != self.repository.head.commit:
                    print("NEW VERSION")
                break
            except:
                time.sleep(1)

    def run(self):
        self.run_loading_frame()
        self.pull()
        import main
        import glob_var
        time.sleep(5)
        glob_var.main_menu_frame = main.MainMenu()
        self.loading_frame.destroy()
        glob_var.main_menu_frame.mainloop()
        exit()

    def run_loading_frame(self):
        self.loading_frame = ctk.CTK()
        self.loading_frame.geometry(glob_style.screen_resolution)

        self.loading_screen_label = ctk.CTkLabel(self.loading_frame, text="Loading...")
        self.loading_screen_label.grid(row=0, column=0)
        self.loading_frame.mainloop()

try:
    deployer = AutoDeployer()
    with open('test.txt', 'w') as f:
        f.write('success')
    deployer.run()

except:
    with open('test.txt', 'w') as f:
        f.write(format_exc())