import subprocess

result = subprocess.run(["checkupdates"], capture_output=True, text=True)
updateable_packages = str(len(result.stdout.splitlines()))
with open("/tmp/aurora.log", "w") as f:
    f.write(f"{updateable_packages}\n")