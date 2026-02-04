from aurora.functions import get_distro
from aurora.config.paths import state_path

def check_updates():
    distro = get_distro()
    updateable_packages = distro.check_updates()
    with open(state_path, "w") as f:
        f.write(updateable_packages)

if __name__ == "__main__":
    check_updates()
