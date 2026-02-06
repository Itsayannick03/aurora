from .driver import Driver
import subprocess
from collections import Counter

class Ubuntu(Driver):
    
    FLAGGED_PACKAGES = Driver.FLAGGED_PACKAGES | {
    "linux-image-generic": {
        "risk": "high",
        "category": "kernel",
    },
    "linux-headers-generic": {
        "risk": "high",
        "category": "kernel",
    },
    "linux-generic": {
        "risk": "high",
        "category": "kernel",
    },
    "initramfs-tools": {
        "risk": "high",
        "category": "boot",
    },
    "grub-pc": {
        "risk": "high",
        "category": "bootloader",
    },
    "grub-efi-amd64": {
        "risk": "high",
        "category": "bootloader",
    },
    "systemd": {
        "risk": "high",
        "category": "core",
    },
    "udev": {
        "risk": "high",
        "category": "core",
    },
    "dbus": {
        "risk": "high",
        "category": "core",
    },
    "libc6": {
        "risk": "critical",
        "category": "core-lib",
    },
    "apt": {
        "risk": "high",
        "category": "package-manager",
    },
    "dpkg": {
        "risk": "high",
        "category": "package-manager",
    },
    "python3": {
        "risk": "low",
        "category": "runtime",
    },
    "openssl": {
        "risk": "medium",
        "category": "crypto",
    },
    "ca-certificates": {
        "risk": "medium",
        "category": "trust",
    },
}

    
    def __init__(self):
        self.dependencies = [
            "python3",
            "apt",
            "systemd",
            
        ]
    
    def update():
        subprocess.run(["sudo", "apt", "upgrade"])

    def check_updates(self):
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if result.returncode == 0 or result.returncode == 2:
            return str(sum(
                1 for line in result.stdout.splitlines()
                if line and not line.startswith("Listing")
            ))

        raise Ubuntu.Error()

    def check_dependencies(self,say=lambda x: None, terminal=lambda x: None, write=lambda x: None):
        say("Since you are using Ubuntu I’ll check the dependencies myself. Apt likes to say things are fine when they’re not.")
        
        missing = []
        
        for item in self.dependencies:
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
                
    def get_pkg_name(self, update_entry):
        split =update_entry.split("/")
        return split[0]
    
    def count_important_packages(self):
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        
        if result.returncode not in (0, 2):
            raise Ubuntu.Error()
        
        names = []
        for entry in result.stdout.splitlines():
            entry = entry.strip()
            if not entry or entry.startswith("Listing"):
                continue
            names.append(self.get_pkg_name(entry))
        
        counts = Counter(names)
        
        res = []
        for pkg_name, meta in self.FLAGGED_PACKAGES.items():
            c = sum(
                count
                for name, count in counts.items()
                if name == pkg_name or name.startswith(pkg_name + "-")
            )
            
            if c == 0:
                continue
           
            res.append({
                "name": pkg_name,
                "count": c,
                "risk": meta["risk"],
                "category": meta["category"],
            })
        return res