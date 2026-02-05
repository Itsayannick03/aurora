from .driver import Driver
import subprocess

class Ubuntu(Driver):

    def __init__(self):
        self.dependencies = [
            "python3",
            "apt",
            "systemd",
        ]
    
    def update():
        subprocess.run(["sudo", "apt", "upgrade"])

    def check_updates(self):
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if result.returncode == 0:
            return str(sum(
                1 for line in result.stdout.splitlines()
                if line and not line.startswith("Listing")
            ))
        raise Ubuntu.Error()

    def check_dependencies(self,say=lambda x: None, terminal=lambda x: None, write=lambda x: None):
        say("Since you are using Ubuntu I’ll check the dependencies myself. Apt likes to say things are fine when they’re not.")
        
        missing = []
        
        for item in self.dependencies:
            check = subprocess.run(["dpkg", "-s", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            say("You are missing some dependencies, typical humans... Don't worry I'll install them for you")
            for item in missing:
                write(f"sudo apt install {item}")
                subprocess.run(["sudo", "apt", "install", item], capture_output=True, text=True)
        
