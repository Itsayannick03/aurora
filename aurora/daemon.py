import subprocess

def check_updates():
    result = subprocess.run(["checkupdates"], capture_output=True, text=True)
    updateable_packages = str(len(result.stdout.splitlines()))
    with open("/tmp/aurora.log", "w") as f:
        f.write(updateable_packages)

if __name__ == "__main__":
    check_updates()
