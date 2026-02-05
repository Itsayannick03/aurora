from time import sleep
import sys
import random
from pathlib import Path
from datetime import datetime
import getpass
import platform
from aurora.drivers.ubuntu import Ubuntu
from aurora.drivers.arch import Archlinux


start = 0.01
end = 0.04
small_start = 0.01
small_end = 0.05



user = getpass.getuser()

def say(message):
    print("Aurora:", end=" ")

    letters = list(message)
    length = len(message)
    for i in range(length):
        print(letters[i], end="")
        sys.stdout.flush()
        sleep(random.uniform(small_start, small_end))
    print(" ", end="")
    sys.stdout.flush()
    sleep(random.uniform(start, end))
    print("")

def write(message):
    try:
        hostname = Path("/etc/hostname").read_text().strip()
    except:
        hostname = "User"
    pwd = Path.cwd()
    print(f"Aurora@{hostname}:{pwd}$", end=" ")

    letters = list(message)
    length = len(message)
    for i in range(length):
        print(letters[i], end="")
        sys.stdout.flush()
        sleep(random.uniform(small_start, small_end))
    print(" ", end="")
    sys.stdout.flush()
    sleep(random.uniform(start, end))
    print("")



def terminal(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"({ts}) {msg}")
    sleep(0.4)

def add_to_bashrc():
    with open(f"/home/{user}/.bashrc", "r") as f:
        if "# Aurora shell hook" in f.read():
            return
    with open(f"/home/{user}/.bashrc", "a") as f:
        f.write("\n# Aurora shell hook\n")
        f.write(f"python {Path.cwd()}/Aurora.py")

def get_distro():
    id_, id_like = get_distro_id()
    if id_ == 'ubuntu':
        return Ubuntu()
    elif id_ == 'archlinux' or id_ == "arch":
        return Archlinux()
    raise RuntimeError("No distro found")
        
def get_distro_id():
    distro = {}
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip().split("=", 1)
                distro[k] = v.strip('"')
    return distro.get("ID"), distro.get("ID_LIKE")
