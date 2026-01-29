import subprocess
from functions import get_distro_id
from config.paths import *

def check_updates():
    id_, id_like = get_distro_id()
    
    if id_ == 'ubuntu':
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if result.returncode == 0:
            updateable_packages = str(sum(
                1 for line in result.stdout.splitlines()
                if line and not line.startswith("Listing")
            ))
        else:
            updateable_packages = "ERROR"

    else:
        result = subprocess.run(["checkupdates"], capture_output=True, text=True)
        if result.returncode == 0:
            updateable_packages = str(len(result.stdout.splitlines()))
        else:
            updateable_packages = "ERROR"
        
    with open(log_path, "w") as f:
        f.write(updateable_packages)

if __name__ == "__main__":
    check_updates()
