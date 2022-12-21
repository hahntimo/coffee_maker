import git
import os
import requests
import time


class AutoDeployer:
    def __init__(self):
        self.branch = "main"
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        self.repository = git.Repo(self.repo_path)

    def check_internet_connection(self):
        for attempt in range(20):
            try:
                requests.head("https://google.com", timeout=1)
                return True
            except:
                time.sleep(1)
        return True

    def deploy(self):
        if self.check_internet_connection():
            self.repository.git.checkout(self.branch)
            current_repo_state = self.repository.head.commit
            self.repository.remotes.origin.pull()

            if current_repo_state != self.repository.head.commit:
                print("NEW VERSION")

            import main
            import glob_var
            glob_var.main_menu_frame = main.MainMenu()
            glob_var.main_menu_frame.mainloop()
            exit()


deployer = AutoDeployer()
deployer.deploy()
