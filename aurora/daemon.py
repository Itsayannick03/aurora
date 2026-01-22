import subprocess
from aurora.functions import get_distro_id
from aurora.config.paths import log_path

def check_updates():
    id_, id_like = get_distro_id()

    if id_ == 'ubuntu':
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        updateable_packages = str(sum(
            1 for line in result.stdout.splitlines()
            if line and not line.startswith("Listing")
        ))
    else:
        result = subprocess.run(["checkupdates"], capture_output=True, text=True, check=True)
        updateable_packages = str(len(result.stdout.splitlines()))
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(updateable_packages)

if __name__ == "__main__":
    check_updates()
