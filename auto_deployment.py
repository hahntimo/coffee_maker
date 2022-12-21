import git
import os
import requests
import time
from traceback import format_exc


class AutoDeployer:
    def __init__(self):
        self.branch = "main"
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.repo_path)
        self.repository = git.Repo(self.repo_path)

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
        self.pull()
        import main
        import glob_var
        glob_var.main_menu_frame = main.MainMenu()
        glob_var.main_menu_frame.mainloop()
        exit()

try:
    deployer = AutoDeployer()
    with open('test.txt', 'w') as f:
        f.write('success')
    deployer.run()

except:
    with open('test.txt', 'w') as f:
        f.write(format_exc())