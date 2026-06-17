from aurora.functions import get_distro
from aurora.config.paths import state_path
import json

def update_cache():
    distro = get_distro()
    package_count = distro.check_updates()
    updates_list = distro.get_pkg_list()

    data = {
        "package_count": package_count,
        "updates_list": updates_list
    }

    with open(state_path, "w") as f:
        json.dump(data, f, indent=4)
    
        
    

def check_updates():
    distro = get_distro()
    updateable_packages = distro.check_updates()
    with open(state_path, "r") as f:
        f.write(updateable_packages)
    
    
def create_list():
    distro = get_distro()
    updates_list = distro.get_pkg_list()
    with open("/tmp/update-list.txt", "w") as f:
        for item in updates_list:
            f.write(item)
            f.write("\n")

if __name__ == "__main__":
    update_cache()
