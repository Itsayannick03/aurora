#!/usr/bin/python
# Aurora - A Arch Linux update assistant
# Copyright (C) 2025 Yannick Winkler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import sys
import os
sys.path.append("/usr/lib/aurora")
import responses

import subprocess
import random
from rich import print
import config


from daemon import check_updates

from functions import get_distro_id, is_arch, is_ubuntu


#---------------- FILE PATHS ----------------
result_storage_file = "/tmp/aurora.log"

# ---------------- FUNCTIONS ----------------
def update():
    if is_arch():
        """Run system update via pacman."""
        subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"])
        # after update we check again
        check_updates()
    elif is_ubuntu():
        """Run system update via apt"""
        subprocess.run(["sudo", "apt", "upgrade"])
        check_updates()
    else:
        raise RuntimeError("Unsupported package manager")

def package_count():
    """Print package count with color according to severity."""
    if updateable_packages < config.normal_threshold:
        color = "green"
    elif updateable_packages < config.moderate_threshold:
        color = "yellow"
    elif updateable_packages < config.high_threshold:
        color = "red"
    else:
        color = "dark_red"

    print(f"[{color}]{updateable_packages}[/{color}] packages require attention.")


def sas_response():
    """Print sassy response according to update stage and whether we ask today."""
    
    if updateable_packages == 0:
            print("Aurora:", random.choice(responses.stage_0))
    elif updateable_packages < config.normal_threshold:
            print("Aurora:", random.choice(responses.stage_1))
    elif updateable_packages < config.moderate_threshold:
            print("Aurora:", random.choice(responses.stage_2))
    elif updateable_packages < config.high_threshold:
            print("Aurora:", random.choice(responses.stage_3))
    elif updateable_packages < config.critical_threshold:
            print("Aurora:", random.choice(responses.stage_4))
    else:
        print("Aurora:", random.choice(responses.stage_5))
    


def update_handler():
    """Handle user prompts or forced updates based on load and stage."""
    sas_response()
    if updateable_packages < config.normal_threshold:
        # Minimal load, no update required
        return

    elif updateable_packages < config.high_threshold and config.ask_update:
        # Moderate to high load, ask user
        valid_responses = ["y", "n"]
        while True:
            print("Aurora: Do you want me to update? (y/n)")
            inpt = input("> ").strip().lower()
            if inpt in valid_responses:
                if inpt == "y":
                    update()
                    with open(result_storage_file, "w") as f:
                        f.write("0")
                break
            else:
                print("Aurora:", random.choice(responses.invalid_input_responses))

    elif updateable_packages >= config.high_threshold and config.auto_update:
        # Forced auto-update
        print("Aurora:", random.choice(responses.aurora_auto_update_responses))
        update()
        with open(result_storage_file, "w") as f:
            f.write("0")


def handle_flags():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("aurora","[--options]","[--actions]")
        print("-h","--help",9*" ","Print this message")
        print("  ","--no-update",4*" ","Prevent aurora from asking to, or, auto updating")
        print("  ","--update",7*" ","Will force check updateable package count")
        exit(0)
        
    if "--no-update" in sys.argv:
        config.ask_update = False
        config.auto_update = False

    if "--update" in sys.argv:
        check_updates()
        

# ---------------- MAIN ----------------
handle_flags()    

try:
    with open("/tmp/aurora.log", "r") as f:        
        updateable_packages = int(f.read().strip())
except FileNotFoundError:
    # if the files doesnt exist we create it by updateing it
    subprocess.run(["systemctl", "--user", "start", "aurora.service"])
    with open("/tmp/aurora.log", "r") as f:        
        updateable_packages = int(f.read().strip())

package_count()
update_handler()
