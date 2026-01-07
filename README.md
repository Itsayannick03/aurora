# Aurora
Aurora is a lightweight Python-based assistant for Arch Linux that tracks available package updates and reacts based on configurable thresholds.
It uses systemd timers to run update checks automatically in the background.
## Requirements
* Arch Linux
* Python 3
* systemd
* pacman-contrib(for checkupdates)
Install dependency:
```bash
sudo pacman -S pacman-contrib 
```
## How it Works
Aurora consists of two parts:
- **Aurora application**  
  Reads the update count, prints status messages, and optionally performs updates.
- **Aurora daemon**  
  A systemd service + timer that periodically checks for available package updates and stores the result.
## Installation
1. Place the Aurora folder in a fixed location (e.g. ~/Aurora).
2. Edit aurora.service file and set User to your username:
```bash
/home/[User]/Aurora/daemon.py
```
3. Run Aurora once:
```bash
python Aurora.py
```
On first run, Aurora will:
- install its systemd service and timer
- reload systemd
- enable and start the timer automatically

No manual systemd commands are required.
## License
GNU General Public License v3
