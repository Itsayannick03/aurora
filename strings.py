import getpass
from config import daemon_timer, boot_timer


user = getpass.getuser()

service = f"""[Unit]
Description=Aurora daemon service

[Service]
Type=oneshot
ExecStart=/usr/bin/python /home/{user}/Aurora/daemon.py """

timer = f"""[Unit]
Description=Run Aurora package counter every {str(daemon_timer)} seconds

[Timer]
OnBootSec={str(boot_timer)}s
OnUnitActiveSec={str(daemon_timer)}s

[Install]
WantedBy=timers.target

 """


greeting = f"""Hello {user}! I’m Aurora your personal system assistant. Let’s get things running."""


