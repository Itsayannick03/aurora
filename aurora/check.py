from aurora.functions import get_distro

distro = get_distro()

def list_packages():
    pkg_list = distro.get_pkg_list()
    
    for pkg in pkg_list:
        if pkg in distro.FLAGGED_PACKAGES:
            print(f"    - {distro.get_pkg_name(pkg)}")

def main():
    num_updates = distro.check_updates()
    
    print("Aurora checked for updates")
    print("───────────────────────────\n")
    print(f"{num_updates} Packages available")
    list_packages()

if __name__ == "__main__":
    main()