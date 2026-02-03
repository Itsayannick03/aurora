from pathlib import Path

log_path = Path("/tmp/aurora.log")
servicePath = Path("/etc/systemd/user/aurora.service")
timerPath = Path("/etc/systemd/user/aurora.timer")
pacman_hook_path = Path("/etc/pacman.d/hooks")