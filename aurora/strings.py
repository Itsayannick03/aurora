import getpass
from aurora.settings import daemon_timer, boot_timer
import os 

user = getpass.getuser()

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

service = f"""[Unit]
Description=Aurora daemon service
After=network.target

[Service]
Type=oneshot
WorkingDirectory={dir_path}
ExecStart=/usr/bin/python3 -m aurora.daemon """

timer = f"""[Unit]
Description=Run Aurora package counter every {str(daemon_timer)} seconds

[Timer]
OnBootSec={str(boot_timer)}s
OnUnitActiveSec={str(daemon_timer)}s

[Install]
WantedBy=timers.target

 """

pacman_hook = f"""[Trigger]
Operation = Upgrade
Type = Package
Target = pacman

[Action]
Description = Running Aurora after pacman upgrade
When = PostTransaction
WorkingDirectory={dir_path}
ExecStart=/usr/bin/python3 -m aurora.daemon
"""

greeting = f"""Hello {user}! I’m Aurora your personal system assistant. Let’s get things running."""


