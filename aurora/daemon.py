from aurora.functions import get_distro
from aurora.config.paths import state_path, important_updates_path
import json
import os
from datetime import datetime, timezone

def check_updates():
    distro = get_distro()
    updateable_packages = distro.check_updates()
    with open(state_path, "w") as f:
        f.write(updateable_packages)
        
def write_json_atomic(path: str, data: dict) -> None:
    tmp_path = path + ".tmp"
    
    # Write complete JSON to a temp file first
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno()) # ensure its on disk
        
        # Atmoic replace
        os.replace(tmp_path, path)
        

def check_important_packages():
    distro = get_distro()
    pkg_list = distro.count_important_packages()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "distro": distro.__class__.__name__.lower(),
        "important_updates": pkg_list,    
    }
    write_json_atomic("/tmp/important-updates.json", payload)

if __name__ == "__main__":
    check_updates()
    check_important_packages()
