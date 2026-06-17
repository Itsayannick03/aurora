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
import platform
import sys
sys.path.append("/usr/lib/aurora")
import aurora.responses as responses

from aurora.functions import get_distro

import subprocess
import random
from rich import print
import aurora.settings as settings

from aurora.config.paths import state_path, is_updating_path, cooldown_file, system_info_path, performance_cache_path
from aurora.daemon import check_updates
from aurora.status import main as status_main
from aurora.check import main as check_main

from datetime import datetime, timedelta

import json
import psutil
import shutil

import tomllib
from pathlib import Path



distro = get_distro()

updateable_packages = 0
is_updating = False


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

    print(f"    [{color}]{updateable_packages}[/{color}] packages require attention.")


def sas_response():
    """Print sassy response according to update stage and whether we ask today."""
    
    if updateable_packages == 0:
            print("Recomendation:", random.choice(responses.stage_0))
    elif updateable_packages < settings.normal_threshold:
            print("Recomendation:", random.choice(responses.stage_1))
    elif updateable_packages < settings.moderate_threshold:
            print("Recomendation:", random.choice(responses.stage_2))
    elif updateable_packages < settings.high_threshold:
            print("Recomendation:", random.choice(responses.stage_3))
    elif updateable_packages < settings.critical_threshold:
            print("Recomendation:", random.choice(responses.stage_4))
    else:
        print("Recomendation:", random.choice(responses.stage_5))
        
        
def load_cooldown_data():
    if not cooldown_file.exists():
        return {
            "no_count": 0,
            "cooldown_until": None
        }

    with open(cooldown_file, "r") as f:
        return json.load(f)

def get_cooldown():
    data = load_cooldown_data()

    cooldown_until = data.get("cooldown_until")

    if cooldown_until is None:
        return None

    cooldown_until = datetime.fromisoformat(cooldown_until)
    current_time = datetime.now()

    cooldown = cooldown_until - current_time

    if cooldown.total_seconds() <= 0:
        return None

    return cooldown
    

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
            
def print_pkgs():
    global distro
    
    pkg_list = distro.get_pkg_list()
    
    for pkg in pkg_list:
        print(f"    - {pkg}")

def update_flag():
    global distro
    
    print("Aurora Update")
    print("─────────────")
    print("Checking for available updates...\n")
    
    check_updates()
    
    pkg_count = distro.check_updates()
    print(f"{pkg_count} Packages can be upgraded:")
    print_pkgs()
    
    
    print("\nPreparing upgrades...\n")
    inpt = input("Proceed with update? [y/N] ").strip().lower()
    if inpt == "y":
        print("Starting system update...\n")
        update()
        
        print("Update complete")
        return
    else:
        print("Update cancelled.")
        return 


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
    if "check" in sys.argv:
        check_updates()
        check_main()
        exit(0)
    if "update" in sys.argv:
        update_flag()
        exit(0)
        
        
    if "--no-update" in sys.argv:
        settings.ask_update = False
        settings.auto_update = False

    if "--update" in sys.argv:
        try:
            check_updates()
        except OSError:
            print("Couldnt fetch")
            
def get_package_manager():
    if shutil.which("pacman"):
        return "pacman"
    if shutil.which("apt"):
        return "apt"
    if shutil.which("dnf"):
        return "dnf"
    if shutil.which("zypper"):
        return "zypper"
    if shutil.which("apk"):
        return "apk"
    return "unknown"

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)


def get_os_info():
    info = {}

    with open("/etc/os-release") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            info[key] = value.strip('"')

    return info

def get_aurora_version():
    pyproject_path = Path("pyproject.toml")

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data["project"]["version"]
            
     

def main():
    global updateable_packages
    # ---------------- MAIN ----------------
    handle_flags()    
    try:
        with open(state_path, "r") as f:
            try:
                updateable_packages = 45#int(f.read().strip())
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
            
    try:
        with open(system_info_path, "r") as f:
            data = json.load(f)
        os_name = data["os_name"]
        kernal = data["kernal"]
        package_manager = data["package_manager"]
        #aurora_version = data["aurora_version"]
        
    except FileNotFoundError:
        # if the files doesnt exist we create it by updateing it
        system_info_path.parent.mkdir(parents=True, exist_ok=True)
        os_info = get_os_info()
        
        os_name = os_info["PRETTY_NAME"]
        kernal = platform.release()
        package_manager = get_package_manager()
        #aurora_version = get_aurora_version()
        
        data = {
            "os_name": os_name,
            "kernal": kernal,
            "package_manager": package_manager,
            #"aurora_version": aurora_version
        }
        
        with open(system_info_path, "w") as f:
            json.dump(data, f, indent=4)
            
    try:
        with open(performance_cache_path, "r") as f:
            data = json.load(f)
            
        ram_total = data["ram_total"]
        ram_used = data["ram_used"]
        ram_percent = data["ram_percent"]
        cpu_usage = data["cpu_usage"]
    except FileNotFoundError:
        performance_cache_path.parent.mkdir(parents=True, exist_ok=True)

        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        
        ram_total = bytes_to_gb(ram.total)
        ram_used = bytes_to_gb(ram.used)
        ram_percent = ram.percent
        
        data = {
            "ram_total": ram_total,
            "ram_used": ram_used,
            "ram_percent": ram_percent,
            "cpu_usage": cpu_usage
        }
        
        with open(performance_cache_path, "w") as f:
            json.dump(data, f, indent=4)
    
    cooldown = get_cooldown()
    if cooldown is not None:
        seconds_left = int(cooldown.total_seconds())
        minutes = seconds_left // 60
        seconds = seconds_left % 60
    
    print("Aurora status")
    print("──────────────")
    print("System")
    print(f"    OS: {os_name}" )
    print(f"    Kernal: {kernal}")
    print(f"    Package manager: {package_manager.upper()}")
    print()
    print("Performance")
    print(f"    CPU usage: {cpu_usage}%")
    print(f"    RAM used: {ram_used}gb / {ram_total}gb ({ram_percent}%)")
    print()
    print("Aurora")
    print("    Aurora version: 1.1.0")
    print(f"    Mode: {'Passive' if settings.ask_update else 'Active'}")
    print(f"    Auto Update: {'[green]Enabled[/green]' if settings.auto_update else '[red]Disabled[/red]'}")
    print(f"    Cooldown: {'inactive' if cooldown is None else f'{minutes} minutes {seconds} seconds'}")
    print()
    print("Updates")
    package_count(updateable_packages)
    update_handler()

if __name__ == "__main__":
    main()
