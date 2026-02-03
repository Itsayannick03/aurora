from .driver import Driver
import subprocess
from aurora.strings import pacman_hook
from aurora.config.paths import *

class Archlinux(Driver):


    def __init__(self):
        self.dependencies = [
            "python",
            "pacman",
            "systemd",
        ]
    
    def update(self):
        return subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"])
        

    def check_updates(self):
        result = subprocess.run(["checkupdates"], capture_output=True, text=True)
        if result.returncode == 0:
            return str(len(result.stdout.splitlines()))
        raise Archlinux.Error()

    def check_dependencies(self, say=lambda x: None , terminal=lambda x:None):
        missing = []

        say("Since you are using arch, my favorite distro btw, I will have to check that you have the right dependencies")
        for item in self.dependencies:
            check = subprocess.run(["pacman", "-Q", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            for item in missing:
                subprocess.run(["sudo", "pacman", "-S", item], capture_output=True, text=True)

    def install_hook(self, write, MAX_TRIES,say=lambda x: None , terminal=lambda x:None):
        say("One more thing. I’m wiring myself directly into pacman.")
        say("Any time pacman updates itself, I’ll know. Instantly.")
        
        for attempt in range(1, MAX_TRIES + 1):
            terminal("Installing pacman hook...")
            try:
                # Creating pacman hook folder if it doesn't exist
                if not pacman_hook_path.exists():
                    say("Pacman doesn’t have a hook directory yet. That’s fine. I’ll make one.")
                    write("sudo mkdir /etc/pacman.d/hooks")
                    terminal("/etc/pacman.d/hooks path not found")
                    terminal("creating path /etc/pacman.d/hooks")
                    subprocess.run(["sudo", "mkdir", "/etc/pacman.d/hooks"])
                    
                    say("Dropping the hook in place.")
                    write("sudo tee /etc/pacman.d/hooks/aurora-pacman-update.hook")
                    subprocess.run(
                        ["sudo", "tee", "/etc/pacman.d/hooks/aurora-pacman-update.hook"],
                        input=pacman_hook,
                        text=True,
                        stdout=subprocess.DEVNULL,
                        check=True,
                    )
                    
                    terminal("pacman update hook successfully installed")
                    say("Done. Pacman moves — I respond.")
                    break
            except Exception as e:
                terminal(f"Installation failed: {e}")
                say("That didn’t work. I’ll try again.")
                if attempt == MAX_TRIES:
                    raise

