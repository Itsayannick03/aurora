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

"""Aurora Auto-Update Module - Checks for updates from the main branch."""

import subprocess
from pathlib import Path
import config



class AuroraUpdater:
    """Checks for and applies Aurora updates from git."""
    
    def __init__(self):
        self.repo_path = Path.cwd()
        self.remote = config.remote
        self.branch = "main"
    
    def _git(self, *args):
        """Run a git command and return the result."""
        return subprocess.run(
            ["git", "-C", str(self.repo_path), *args],
            capture_output=True,
            text=True
        )
    
    def check_for_updates(self):
        """
        Check if updates are available.
        
        Returns:
            tuple: (has_updates: bool, commits_behind: int, error: str or None)
        """
        # Verify git repo
        if self._git("rev-parse", "--git-dir").returncode != 0:
            return False, 0, "Not a git repository"
        
        # Fetch remote
        if self._git("fetch", self.remote, self.branch).returncode != 0:
            return False, 0, "Could not fetch from remote"
        
        # Get local and remote commits
        local = self._git("rev-parse", "HEAD").stdout.strip()
        remote = self._git("rev-parse", f"{self.remote}/{self.branch}").stdout.strip()
        
        if local == remote:
            return False, 0, None
        
        # Count commits behind
        result = self._git("rev-list", "--count", f"HEAD..{self.remote}/{self.branch}")
        commits_behind = int(result.stdout.strip()) if result.returncode == 0 else 0
        
        return True, commits_behind, None
    
    def apply_update(self):
        """Pull latest changes. Returns True if successful."""
        return self._git("pull", self.remote, self.branch).returncode == 0
    
    def notify(self, commits_behind):
        """Print update notification."""
        from rich import print as rprint
        
        rprint("\n[bold cyan]━━━ Aurora Update Available ━━━[/bold cyan]")
        rprint(f"[yellow]A new version is available! ({commits_behind} commit{'s' if commits_behind != 1 else ''} behind)[/yellow]")
        rprint("[cyan]Run 'git pull' to update.[/cyan]")
        rprint("[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n")


def check_aurora_updates():
    """
    Check for Aurora updates and notify user if available.
    
    Args:
        prompt: If True, ask user to update.
    """
    updater = AuroraUpdater()
    has_updates, commits_behind, error = updater.check_for_updates()
    
    if error:
        return
    
    if has_updates:
        updater.notify(commits_behind)
        
        if config.ask_aurora_update:
            from rich import print as rprint
            rprint("[bold]Update now? (y/n)[/bold]")
            if input("> ").strip().lower() in ("y", "yes"):
                if updater.apply_update():
                    rprint("[green] Updated! Please restart Aurora.[/green]\n")
                else:
                    rprint("[red] Update failed. Try manually.[/red]\n")


if __name__ == "__main__":
    check_aurora_updates()
