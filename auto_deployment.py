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

        main.run()
        exit()


if __name__ == "__main__":
    try:
        deployer = AutoDeployer()
        deployer.run()

    except:
        error = format_exc()
        print(error)
        with open('error.txt', 'w') as f:
            f.write(error)