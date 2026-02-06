from typing import Set, List


class Driver:
    #  "linux", "linux-lts", "systemd", "glibc", "openssl", "python"
    # A list of important packages 
    FLAGGED_PACKAGES: Set[str] = {
        # Common baseline for all distros
        "linux": {
            "risk": "high",
            "category": "kernel",
        },
        
        "linux-lts": {
            "risk": "high",
            "category": "kernel",
        },
        
        "systemd": {
            "risk": "high",
            "category": "init",
        },
        
        "glibc": {
            "risk": "critical",
            "category": "core-lib",
        },
        
        "openssl": {
            "risk": "medium",
            "category": "crypto",
        },
        
        "python": {
            "risk": "medium",
            "category": "runtime",
        },
        
        
        
    }
    
    # need self.dependencies
    class Error(Exception):
        pass
    
    
    def update():
        pass
    def check_updates() -> str:
        pass
    def get_updates_list() -> str:
        pass
    # TODO fix this mess
    # its for the fast install
    def check_dependencies(self,say=lambda x: None, terminal=lambda x: None):
        pass
    def install_hook(self, write, MAX_TRIES,say=lambda x: None , terminal=lambda x:None):
        pass
    # For the update urgency check
    def count_important_packages(self):
        return

