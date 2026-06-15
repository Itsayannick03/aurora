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

# TO RUN python -m aurora.main
import os
import sys
sys.path.append("/usr/lib/aurora")
import aurora.responses as responses

from aurora.functions import get_distro

import subprocess
import random
from rich import print
import aurora.settings as settings

from aurora.config.paths import state_path, is_updating_path, cache_path
from aurora.daemon import check_updates
from aurora.status import main as status_main

from datetime import datetime, timedelta

import json


updateable_packages = 0
is_updating = False

cooldown_file = cache_path / "update-cooldown.json"

# ---------------- FUNCTIONS ----------------
def update():
    global updateable_packages
    global is_updating
    global cooldown_file
    
    distro = get_distro()
    
    cooldown_file.unlink(missing_ok=True)

    is_updating = True
    with open(is_updating_path, "w") as f:
        f.write("True")

    distro.update()

    os.remove(is_updating_path)
    is_updating = False
    
    try:
        updateable_packages = distro.check_updates()
    except Exception as e:
        print("Couldn't check updates:", e)
        exit(1)

def package_count(updateable_packages):
    """Print package count with color according to severity."""
    if updateable_packages < settings.normal_threshold:
        color = "green"
    elif updateable_packages < settings.moderate_threshold:
        color = "yellow"
    elif updateable_packages < settings.high_threshold:
        color = "red"
    else:
        color = "dark_red"

    print(f"[{color}]{updateable_packages}[/{color}] packages require attention.")


def sas_response():
    """Print sassy response according to update stage and whether we ask today."""
    
    if updateable_packages == 0:
            print("Aurora:", random.choice(responses.stage_0))
    elif updateable_packages < settings.normal_threshold:
            print("Aurora:", random.choice(responses.stage_1))
    elif updateable_packages < settings.moderate_threshold:
            print("Aurora:", random.choice(responses.stage_2))
    elif updateable_packages < settings.high_threshold:
            print("Aurora:", random.choice(responses.stage_3))
    elif updateable_packages < settings.critical_threshold:
            print("Aurora:", random.choice(responses.stage_4))
    else:
        print("Aurora:", random.choice(responses.stage_5))
        
        
def load_cooldown_data():
    if not cooldown_file.exists():
        return {
            "no_count": 0,
            "cooldown_until": None
        }

    with open(cooldown_file, "r") as f:
        return json.load(f)
    

def save_cooldown_data(data):
    cooldown_file.parent.mkdir(parents=True, exist_ok=True)

    with open(cooldown_file, "w") as f:
        json.dump(data, f, indent=4)
        

def should_ask_update():
    global cooldown_file
    
    if not cooldown_file.is_file():
        return True
    
    data = load_cooldown_data()
    
    cooldown_until = datetime.fromisoformat(data["cooldown_until"])
        
    current_time = datetime.now()
    
    if current_time >= cooldown_until:
        return True
    
    return False


        

def update_handler():
    """Handle user prompts or forced updates based on load and stage."""
    global is_updating
    global cooldown_file
    sas_response()

    if is_updating_path.is_file():
        is_updating = True
        
    if updateable_packages < settings.normal_threshold:
        # Minimal load, no update required
        return
    
    if not should_ask_update():
        return

    elif updateable_packages < settings.high_threshold and settings.ask_update and not is_updating:
        # Moderate to high load, ask user
        valid_responses = ["y", "n"]

        while True:
            print("Aurora: Do you want me to update? (y/n)")
            inpt = input("> ").strip().lower()
            if inpt in valid_responses:
                if inpt == "y":
                    update()
                    with open(state_path, "w") as f:
                        f.write("0")
                else:
                    cooldown_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    data = load_cooldown_data()
                    
                    no_count = int(data["no_count"]) + 1
                    
                    cooldown_time = min(settings.base_cooldown_time * no_count * 2, settings.max_cooldown)
                    
                    current_time = datetime.now()
                    cooldown_until = current_time + timedelta(seconds=cooldown_time)
                    
                    new_data = {
                        "no_count": no_count,
                        "cooldown_until": str(cooldown_until)
                    }
                    
                    save_cooldown_data(new_data)
                    
                    break
            else:
                print("Aurora:", random.choice(responses.invalid_input_responses))

    elif updateable_packages >= settings.high_threshold and settings.auto_update:
        # Forced auto-update
        print("Aurora:", random.choice(responses.aurora_auto_update_responses))
        update()
        with open(state_path, "w") as f:
            f.write("0")


def handle_flags():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("aurora","[--options]","[--actions]")
        print("-h","--help",9*" ","Print this message")
        print("  ","status",9*" ","Will generate a status about the packages missing")
        print("  ","--no-update",4*" ","Prevent aurora from asking to, or, auto updating")
        print("  ","--update",7*" ","Will force check updateable package count")

        exit(0)

    if "status" in sys.argv:
        status_main()
        exit(0)
        
    if "--no-update" in sys.argv:
        settings.ask_update = False
        settings.auto_update = False

    if "--update" in sys.argv:
        try:
            check_updates()
        except OSError:
            print("Couldnt fetch")
            
     

def main():
    global updateable_packages
    # ---------------- MAIN ----------------
    handle_flags()    
    try:
        with open(state_path, "r") as f:
            try:
                updateable_packages = int(f.read().strip())
            except ValueError:
                print("Aurora couldn't fetch updateable packages")
                exit(1)
    except FileNotFoundError:
        # if the files doesnt exist we create it by updateing it
        try:
            updateable_packages = check_updates()
        except Exception as e:
            print("Couldn't fetch updates:", e)
            exit(1)
        subprocess.run(["systemctl", "--user", "start", "aurora.service"])
        with open(state_path, "r") as f:        
            updateable_packages = int(f.read().strip())
    
    package_count(updateable_packages)
    update_handler()

if __name__ == "__main__":
    main()
