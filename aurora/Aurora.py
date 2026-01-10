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

# ---------------- FILE & STATE ----------------
script_dir = os.getenv("HOME")+"/.config"
flag_file = os.path.join(script_dir, ".aurora_update_flag")
time_flag_file = os.path.join(script_dir, ".aurora_time_flag")
result_storage_file = os.path.join(script_dir, ".aurora_result_storage_file")

# ---------------- FUNCTIONS ----------------

def update():
    """Run system update via pacman."""
    subprocess.run(["sudo", "pacman", "-Syu", "--noconfirm"])
    # after update we check again
    check_updates()

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
            print("Aurora:", random.choice(responses.stage_2_update))
    elif updateable_packages < config.high_threshold:
            print("Aurora:", random.choice(responses.stage_3_update))
    elif updateable_packages < config.critical_threshold:
            print("Aurora:", random.choice(responses.stage_4_update))
    else:
        print("Aurora:", random.choice(responses.stage_5))
    


def update_handler():
    """Handle user prompts or forced updates based on load and stage."""
    sas_response()
    if updateable_packages < config.normal_threshold:
        # Minimal load, no update required
        return

    elif updateable_packages < config.high_threshold:
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


# ---------------- MAIN ----------------
#Check if pacman-contrib is installed
check = subprocess.run(["pacman", "-Q", "pacman-contrib"], capture_output=True, text=True)


if check.returncode != 0:
    print("Aurora:", random.choice(responses.missing_contrib))
else:
    try:
        with open("/tmp/aurora.log", "r") as f:        
            updateable_packages = int(f.read().strip())
    except FileNotFoundError:
        # if the files doesnt exist we create it by updateing it
        subprocess.run(["sudo", "systemctl", "start", "aurora.service"])
        with open("/tmp/aurora.log", "r") as f:        
            updateable_packages = int(f.read().strip())

            
package_count()
update_handler()
