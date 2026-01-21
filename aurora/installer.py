import subprocess
from strings import service, timer, greeting,pacman_hook
from functions import say, write, terminal, add_to_bashrc, get_distro_id, is_arch, is_ubuntu
from pathlib import Path
from time import sleep
import random
from config import fast_install, install_shell_hook, DEPENDENCIES
import platform


### Definitions ###
MAX_TRIES = 3

servicePath = Path("/etc/systemd/user/aurora.service")
timerPath = Path("/etc/systemd/user/aurora.timer")
logPath = Path("/tmp/aurora.log")
pacman_hook_path = Path("/etc/pacman.d/hooks")

compatible_os = ["linux"]
compatible_distros = ["arch", "ubuntu"]

if not fast_install:
    say(greeting)

    say("Alright. Let’s set this up properly before you hurt yourself.")
    
    #Compatabilty check
    distro = get_distro_id()[0]
    say("Firstly I need to check what distro you are using.")
    
    ## Some write to find os here !!!!
    os = str(platform.system())
    
    if os.lower() in compatible_os:
        say(f"Ahh {os} perfekt!")
    else:
        say(f"wtf is {os}? I do not support that shit")
    
    say("Now I need to make sure we are compatible")
    distro = str(get_distro_id()[0])
    
    if distro.lower() in compatible_distros:
        say(f"Perfekt! you are using {distro}, you actually did your homework for once")
    else:
        say(f"seriously? {os}, did you even try to read the installation instructions?")
    
    #Dependencies check
    say(f"Now I have to check that you have the right dependencies for {os}:{distro}")
    missing = []
    
    if is_arch():
        say("Since you are using arch, my favorite distro btw, I will have to check that you have the right dependencies")
        dependencies = DEPENDENCIES["arch"]
        for item in dependencies:
            check = subprocess.run(["pacman", "-Q", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            for item in missing:
                subprocess.run(["sudo", "pacman", "-S", item], capture_output=True, text=True)
    
    elif is_ubuntu():
        dependencies = DEPENDENCIES["ubuntu"]
        say("Since you are using Ubuntu I’ll check the dependencies myself. Apt likes to say things are fine when they’re not.")
        
        for item in dependencies:
            check = subprocess.run(["dpkg", "-s", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            say("You are missing some dependencies, typical humans... Don't worry I'll install them for you")
            for item in missing:
                write(f"sudo apt install {item}")
                subprocess.run(["sudo", "apt", "install", item], capture_output=True, text=True)
           
    
    # Checking for existing service and timer files and removing them if they exist
    if servicePath.exists():
        say("Existing service detected. I’ll clean that up.")
        say("This might ask for your password. Depends on how recently you proved you’re allowed to do things.")
        write(f"sudo rm {servicePath}")
        try:
            terminal("removing existing aurora.service...")
            subprocess.run(["sudo", "rm", servicePath])
            sleep(random.uniform(0.5, 5))
            terminal("aurora.service removed.")
        except Exception as err:
            terminal("Task failed.")
            terminal(f"Error: {err}")

    if timerPath.exists():
        say("Existing timer detected. Same fate.")
        write(f"sudo rm {timerPath}")
        try:
            terminal("removing existing aurora.timer...")
            subprocess.run(["sudo", "rm", timerPath])
            sleep(random.uniform(0.5, 5))
            terminal("aurora.timer removed.")
        except Exception as err:
            terminal("Task failed.")
            terminal(f"Error: {err}")

    say("Old files cleared. As expected.")

    base_dir = Path(__file__).resolve().parent

    say("Now we put the new pieces where they belong.")

    if not servicePath.exists() or not timerPath.exists():
        say("Installing systemd service.")
        write(f'"sudo", "tee", "{servicePath}\n{service}"')
        terminal("installing aurora.service...")
        sleep(random.uniform(0.5, 5))
        try:
            subprocess.run(
                ["sudo", "tee", servicePath],
                input=service,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal("aurora.service installed.")
        except Exception as err:
            terminal("Installation failed.")
            terminal(f"Error: {err}")

        say("Installing systemd timer.")
        write(f'"sudo", "tee", "{timerPath}\n{timer}"')
        terminal("installing aurora.timer...")
        sleep(random.uniform(0.5, 5))
        try:
            subprocess.run(
                ["sudo", "tee", timerPath],
                input=timer,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal("aurora.timer installed.")
        except Exception as err:
            terminal("Installation failed.")
            terminal(f"Error: {err}")
        
       

        if is_arch():
            say("One more thing. I’m wiring myself directly into pacman.")
            say("Any time pacman updates itself, I’ll know. Instantly.")
            
            for attempt in range(1, MAX_TRIES + 1):
                terminal("Installing pacman hook...")
                try:
                    # Creating pacman hook folder if it doesn't exist
                    if not pacman_hook_path.exists():
                        say("Pacman doesn’t have a hook directory yet. That’s fine. I’ll make one.")
                        write("sudo mkdir /etc/pacman.d/hooks")
                        terminal("/etc/pacman.d/hooks path not found")
                        terminal("creating path /etc/pacman.d/hooks")
                        subprocess.run(["sudo", "mkdir", "/etc/pacman.d/hooks"])

                    say("Dropping the hook in place.")
                    write("sudo tee /etc/pacman.d/hooks/aurora-pacman-update.hook")
                    subprocess.run(
                        ["sudo", "tee", "/etc/pacman.d/hooks/aurora-pacman-update.hook"],
                        input=pacman_hook,
                        text=True,
                        stdout=subprocess.DEVNULL,
                        check=True,
                    )

                    terminal("pacman update hook successfully installed")
                    say("Done. Pacman moves — I respond.")
                    break
                except Exception as e:
                    terminal(f"Installation failed: {e}")
                    say("That didn’t work. I’ll try again.")
                    if attempt == MAX_TRIES:
                        raise

        say("Refreshing systemd. It likes to be told when things change.")
        say("I’ll need your password for this part. Don’t worry, I’m not interested in it.")
        write("systemctl --user daemon-reload")
        if subprocess.run(["systemctl", "--user", "daemon-reload"]).returncode != 0:
            say("systemd did not cooperate.")

        say("Activating Aurora.")
        say("I’ll need your password once more. Relax, If I wanted it, you’d never know.")
        write("systemctl --user enable --now aurora.timer")
        if subprocess.run(["systemctl", "--user", "enable", "--now", "aurora.timer"]).returncode != 0:
            say("Activation failed.")

    say("Service and timer files are ready. Try to keep up.")

    say("One last thing. Want Aurora available automatically in your terminal? (y/n)")

    valid_responses = ["y", "n", "yes", "no"]
    while True:
        inpt = input("> ").strip().lower()
        if inpt in valid_responses:
            if inpt == "y" or inpt == "yes":
                add_to_bashrc()
            break
        else:
            say("Focus. It’s a yes or a no question it ain' that hard. y or n.")
    say("That’s it. I’m in place now. I’ll take it from here—try not to make my job harder.")
    
# Fast install
else:
    #Compatabilty check
    terminal(":: Checking system compatibility")
    
    os = str(platform.system())
    
    if os.lower() in compatible_os:
        terminal(f"[ OK ] Operating system: {os}")
    else:
        terminal(f"[ FAIL ] Operating system: {os} (unsupported)")
    
    distro = str(get_distro_id()[0])
    if distro.lower() in compatible_distros:
        terminal(f"[ OK ] Distribution: {distro}")
    else:
        terminal(f"[ FAIL ] Distribution: {distro} (unsupported)")
    
    #Dependencies check
    terminal(f":: Checking dependencies for {os}:{distro}")
    missing = []
    
    if is_arch():
        dependencies = DEPENDENCIES["arch"]
        for item in dependencies:
            check = subprocess.run(["pacman", "-Q", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            for item in missing:
                subprocess.run(["sudo", "pacman", "-S", item], capture_output=True, text=True)
    
    elif is_ubuntu():
        dependencies = DEPENDENCIES["ubuntu"]
        
        for item in dependencies:
            check = subprocess.run(["dpkg", "-s", item], capture_output=True, text=True)
            if check.returncode == 0:
                terminal(f"[ OK ] {item}")
            else:
                terminal(f"[ FAIL ] {item}")   
                missing.append(item)
                
        if len(missing) > 0:
            for item in missing:
                subprocess.run(["sudo", "apt", "install", item], capture_output=True, text=True)
           
    
    # Deleting old service file
    if servicePath.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal("deleting old aurora.service file, this might require sudo authentication")
                subprocess.run(["sudo", "rm", servicePath])
                terminal("deleted aurora.service")
                break
            except Exception as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise
    # Deleting old timer files
    if timerPath.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal("deleting old aurora.timer file, this might require sudo authentication")
                subprocess.run(["sudo", "rm", timerPath])
                terminal("deleted aurora.timer")
                break
            except Exception as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise
    # Deleting aurora log
    if logPath.exists():
        for attempt in range(1, MAX_TRIES + 1):
            try:
                terminal("deleting old aurora.log file, this might require sudo authentication")
                subprocess.run(["sudo", "rm", "/tmp/aurora.log"], check=True)
                terminal("succesfully deleted aurora.log")
                break
            except subprocess.CalledProcessError as e:
                terminal(f"Attempt {attempt} failed: {e}")
                if attempt == MAX_TRIES:
                    raise
    # Installing service file
    for attempt in range(1, MAX_TRIES + 1):
        try:
            terminal("Installing service file")
            subprocess.run(
                ["sudo", "tee", servicePath],
                input=service,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal("service file sucefsfully installed")
            break
        except Exception as e:
            terminal(f"Installation failed: {e}")
            if attempt == MAX_TRIES:
                raise
    # Installing timer file
    for attempt in range(1, MAX_TRIES + 1):
        try:
            terminal("Installing timer file")
            subprocess.run(
                ["sudo", "tee", timerPath],
                input=timer,
                text=True,
                stdout=subprocess.DEVNULL,
                check=True,
            )
            terminal("timer file sucefsfully installed")
            break
        except Exception as e:
            terminal(f"Installation failed: {e}")
            if attempt == MAX_TRIES:
                raise
    # Instaling pacman hook
    if is_arch():
        for attempt in range(1, MAX_TRIES + 1):
            terminal("Installing pacman hook")
            try:
                # Creating pacman hook folder if it doesn't exist 
                if not pacman_hook_path.exists():
                    terminal("/etc/pacman.d/hooks path not found")
                    terminal("creating path /etc/pacman.d/hooks")
                    subprocess.run(["sudo", "mkdir", "/etc/pacman.d/hooks"])
                subprocess.run(
                    ["sudo", "tee", "/etc/pacman.d/hooks/aurora-pacman-update.hook"],
                    input=pacman_hook,
                    text=True,
                    stdout=subprocess.DEVNULL,
                    check=True,
                )
                terminal("pacman update hook sucefsfully installed")
                break
            except Exception as e:
                terminal(f"Installation failed: {e}")
                if attempt == MAX_TRIES:
                    raise
    # Reloading daemon
    for attempt in range(1, MAX_TRIES + 1):
        terminal("Reloading daemon services")
        try:
            subprocess.run(["systemctl", "--user", "daemon-reload"])
            terminal("Daemon services sucessfully reloaded")
            break
        except Exception as e:
            terminal(f"Failed to reload daemon services: {e}")
            if attempt == MAX_TRIES:
                raise
    # enableing aurora timer
    for attemt in range(1, MAX_TRIES + 1):
        terminal("Enableing aurora timer")
        try:
            subprocess.run(["systemctl", "--user", "enable", "--now", "aurora.timer"])
            terminal("aurora timer sucessfully enabled")
            break
        except Exception as e:
            terminal(f"Failed to enable aurora timer: {e}")
            if attempt == MAX_TRIES:
                raise
    # Writing aurora into bashrc file
    if install_shell_hook:
        for attempt in range(1, MAX_TRIES + 1):
            terminal("Adding aurora script to bashrc file")
            try:
                add_to_bashrc()
                terminal("Sucessfully added aurora script to bashrc file")
                break
            except Exception as e:
                terminal(f"Failed to add aurora script to bashrc file: {e}")
                if attempt == MAX_TRIES:
                    raise
    
    terminal("Installation complete")
# Running daemon once
subprocess.run(["systemctl", "--user", "start", "aurora.service"])

    


