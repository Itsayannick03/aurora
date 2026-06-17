from pathlib import Path


is_updating_path = Path("/tmp/aurora-is-updating")
state_path = Path("/tmp/aurora.log")
important_updates_path = Path("/tmp/important-updates.json")
servicePath = Path("/etc/systemd/user/aurora.service")
timerPath = Path("/etc/systemd/user/aurora.timer")
pacman_hook_path = Path("/etc/pacman.d/hooks")
cache_path = Path("/tmp/")
system_info_path = Path("/tmp//system.json")
performance_cache_path = Path("/tmp/performance.json")
cooldown_file = cache_path / "update-cooldown.json"
