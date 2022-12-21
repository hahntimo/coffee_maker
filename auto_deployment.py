import git
import os


class AutoDeployer:
    def __init__(self):
        self.branch = "main"
        self.repository = git.Repo(os.path.dirname(os.path.abspath("__main__")))

    def deploy(self):
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
