from pathlib import Path

state_path = Path("/tmp/aurora.log")
important_updates_path = Path("/tmp/important-updates.json")
servicePath = Path("/etc/systemd/user/aurora.service")
timerPath = Path("/etc/systemd/user/aurora.timer")
pacman_hook_path = Path("/etc/pacman.d/hooks")