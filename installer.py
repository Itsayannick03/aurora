import subprocess
from aurora.strings import service, timer, greeting
from aurora.functions import say, write, terminal, add_to_bashrc, get_distro, get_distro_id
from pathlib import Path
from time import sleep
import random
from aurora.settings import fast_install, install_shell_hook, install_command_symlink
import platform
from aurora.config.paths import state_path, servicePath, timerPath, symlink_path
import sys
import getpass

### Definitions ###
MAX_TRIES = 3

if "--fast" in sys.argv:
    fast_install = True

compatible_os = ["linux"]
compatible_distros = ["arch", "ubuntu"]

valid_responses = ["y", "n", "yes", "no"]

yes_input = ["y", "yes"]
no_input = ["n", "no"]

# get user
user = getpass.getuser()

# get current distro
disto = get_distro()

if not fast_install:
    say(greeting)

    say(":: Preparing Aurora installation")

    distro = get_distro_id()[0]
    say(":: Detecting operating system")

    os = str(platform.system())

    if os.lower() in compatible_os:
        say(f":: Operating system detected: {os}")
    else:
        say(f":: Unsupported operating system: {os}")

    say(":: Detecting Linux distribution")

    distro = str(get_distro_id()[0])

    if distro.lower() in compatible_distros:
        say(f":: Distribution detected: {distro}")
    else:
        say(f":: Unsupported distribution: {distro}")

    say(f":: Checking dependencies for {os}:{distro}")

    disto.check_dependencies(say, terminal)

    if servicePath.exists():
        say(":: Existing aurora.service detected")
        write(f"sudo rm {servicePath}")
        try:
            terminal(":: Removing aurora.service")
            subprocess.run(["sudo", "rm", servicePath])
            sleep(random.uniform(0.5, 5))
            terminal(":: aurora.service removed")
        except Exception as err:
            terminal(":: Task failed")
            terminal(f":: Error: {err}")

    if timerPath.exists():
        say(":: Existing aurora.timer detected")
        write(f"sudo rm {timerPath}")
        try:
            terminal(":: Removing aurora.timer")
            subprocess.run(["sudo", "rm", timerPath])
            sleep(random.uniform(0.5, 5))
            terminal(":: aurora.timer removed")
        except Exception as err:
            terminal(":: Task failed")
            terminal(f":: Error: {err}")

    say(":: Old files cleared")

    base_dir = Path(__file__).resolve().parent

    say(":: Installing system components")

    if not servicePath.exists() or not timerPath.exists():

        say(":: Installing aurora.service")
        write(f'"sudo", "tee", "{servicePath}\n{service}"')
        terminal(":: Installing aurora.service")
        sleep(random.uniform(0.5, 5))

        try:
            subprocess.run(
                ["sudo", "tee", servicePath],
                input=service,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal(":: aurora.service installed")
        except Exception as err:
            terminal(":: Installation failed")
            terminal(f":: Error: {err}")

        say(":: Installing aurora.timer")
        write(f'"sudo", "tee", "{timerPath}\n{timer}"')
        terminal(":: Installing aurora.timer")
        sleep(random.uniform(0.5, 5))

        try:
            subprocess.run(
                ["sudo", "tee", timerPath],
                input=timer,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal(":: aurora.timer installed")
        except Exception as err:
            terminal(":: Installation failed")
            terminal(f":: Error: {err}")

        disto.install_hook(write, MAX_TRIES, say, terminal)

        say(":: Reloading systemd user daemon")
        write("systemctl --user daemon-reload")

        if subprocess.run(["systemctl", "--user", "daemon-reload"]).returncode != 0:
            say(":: systemd reload failed")

        say(":: Enabling aurora timer")
        write("systemctl --user enable --now aurora.timer")

        if subprocess.run(["systemctl", "--user", "enable", "--now", "aurora.timer"]).returncode != 0:
            say(":: Timer activation failed")

    say(":: Service and timer setup complete")

    say(":: Install command symlink so 'aurora' can be run globally? [Y/n]")

    if input(":: ").strip().lower() not in no_input:

        aurora_main_path = Path.cwd() / "Aurora.py"

        if symlink_path.exists():
            say(":: Existing symlink detected. Reinstall it? [y/N]")

            if input(":: ").strip().lower() in yes_input:

                write(f"sudo rm -rf {symlink_path}")
                subprocess.run(["sudo", "rm", "-rf", symlink_path])
                terminal(f":: {symlink_path} removed")

                say(":: Creating new symlink")
                write(f"sudo ln -s {aurora_main_path} {symlink_path}")
                subprocess.run(["sudo", "ln", "-s", aurora_main_path, symlink_path])
                terminal(":: Symlink installed")

        else:
            say(":: Creating symlink")
            write(f"sudo ln -s {aurora_main_path} {symlink_path}")
            subprocess.run(["sudo", "ln", "-s", aurora_main_path, symlink_path])
            terminal(":: Symlink installed")

    say(":: Add Aurora to your shell startup (.bashrc)? [y/N]")

    while True:
        inpt = input(":: ").strip().lower()

        if inpt in valid_responses:
            if inpt in yes_input:
                add_to_bashrc()
            break
        else:
            say(":: Please answer y or n")

    say(":: Installation complete")

# Fast install
else:

    terminal(":: Checking system compatibility")

    os = str(platform.system())

    if os.lower() in compatible_os:
        terminal(f"[ OK ] Operating system: {os}")
    else:
        terminal(f"[ FAIL ] Operating system: {os} (unsupported)")
        sys.exit(1)

    distro = str(get_distro_id()[0])

    if distro.lower() in compatible_distros:
        terminal(f"[ OK ] Distribution: {distro}")
    else:
        terminal(f"[ FAIL ] Distribution: {distro} (unsupported)")

    terminal(f":: Checking dependencies for {os}:{distro}")

    disto.check_dependencies(terminal=terminal)

    if servicePath.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal(":: Removing old aurora.service")
                subprocess.run(["sudo", "rm", servicePath])
                terminal(":: aurora.service removed")
                break
            except Exception as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise

    if timerPath.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal(":: Removing old aurora.timer")
                subprocess.run(["sudo", "rm", timerPath])
                terminal(":: aurora.timer removed")
                break
            except Exception as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise

    if state_path.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal(":: Removing old aurora.log")
                subprocess.run(["sudo", "rm", state_path], check=True)
                terminal(":: aurora.log removed")
                break
            except subprocess.CalledProcessError as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise

    for attempt in range(1, MAX_TRIES + 1):
        try:
            terminal(":: Installing service file")
            subprocess.run(
                ["sudo", "tee", servicePath],
                input=service,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal(":: Service file installed")
            break
        except Exception as e:
            terminal(f"Installation failed: {e}")
            if attempt == MAX_TRIES:
                raise

    for attempt in range(1, MAX_TRIES + 1):
        try:
            terminal(":: Installing timer file")
            subprocess.run(
                ["sudo", "tee", timerPath],
                input=timer,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal(":: Timer file installed")
            break
        except Exception as e:
            terminal(f"Installation failed: {e}")
            if attempt == MAX_TRIES:
                raise

    disto.install_hook(write, MAX_TRIES, terminal=terminal)

    for attempt in range(1, MAX_TRIES + 1):
        terminal(":: Reloading daemon services")

        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"])
            terminal(":: Daemon reloaded")
            break
        except Exception as e:
            terminal(f"Failed to reload daemon: {e}")
            if attempt == MAX_TRIES:
                raise

    for attempt in range(1, MAX_TRIES + 1):
        terminal(":: Enabling aurora timer")

        try:
            subprocess.run(["systemctl", "--user", "enable", "--now", "aurora.timer"])
            terminal(":: Timer enabled")
            break
        except Exception as e:
            terminal(f"Failed to enable timer: {e}")
            if attempt == MAX_TRIES:
                raise

    terminal(":: Add Aurora to your .bashrc so it loads automatically? [y/N]")

    response = input(":: ").strip().lower()

    if response in yes_input:

        for attempt in range(1, MAX_TRIES + 1):
            terminal(":: Updating .bashrc")

            try:
                add_to_bashrc()
                terminal(":: .bashrc updated")
                break
            except Exception as e:
                terminal(f"Failed to update .bashrc: {e}")
                if attempt == MAX_TRIES:
                    raise

    if install_command_symlink:

        terminal(":: Installing command symlink")

        aurora_main_path = Path.cwd() / "Aurora.py"

        if symlink_path.exists():

            terminal(":: Existing symlink detected. Reinstall it? [y/N]")

            if input(":: ").strip().lower() in yes_input:
                subprocess.run(["sudo", "rm", "-rf", symlink_path])
                terminal(f":: {symlink_path} removed")

                terminal(":: Creating new symlink")
                subprocess.run(["sudo", "ln", "-s", aurora_main_path, symlink_path])

        else:
            terminal(":: Creating symlink")
            subprocess.run(["sudo", "ln", "-s", aurora_main_path, symlink_path])
            terminal(":: Symlink installed")

    terminal(":: Installation complete")

# Running daemon once
subprocess.run(["systemctl", "--user", "start", "aurora.service"])