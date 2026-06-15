# Aurora

Aurora is a lightweight Python-based update assistant for Linux. It checks for available package updates, keeps track of the current update state, and gives clear terminal output based on how important the pending updates are.

Aurora is designed to be simple, fast, and distribution-aware. The long-term goal is to support many different Linux distributions and package managers through one clean assistant interface.

Currently supported distributions:

* Arch Linux
* Ubuntu

More distributions may be added in the future.

Aurora is not meant to blindly update your system without your input. Instead, it gives you a quick overview of your system’s update situation and can help you decide when it is time to update. It can show how many packages are waiting, assign a severity level, provide details, and print a recommendation based on the current state.

Aurora uses systemd services and timers to run update checks automatically in the background. The latest result is stored locally, so commands like `aurora` and `aurora status` can quickly display the current update state without needing to perform a full update check every time.

## Features

* Checks for available system package updates
* Supports Arch Linux and Ubuntu
* Designed to support more Linux distributions in the future
* Uses systemd timers for automatic background update checks
* Stores the latest update state locally
* Provides a main assistant command with `aurora`
* Provides a status overview with `aurora status`
* Shows update severity, package count, summary, details, and recommendations
* Supports configurable update thresholds
* Can optionally help start the system update process
* Lightweight and terminal-friendly

## Supported Distributions

Aurora currently supports:

### Arch Linux

On Arch Linux, Aurora uses Arch package management tools to check for updates.

Aurora depends on `checkupdates`, which is provided by `pacman-contrib`.

Install it with:

```bash
sudo pacman -S pacman-contrib
```

### Ubuntu

On Ubuntu, Aurora uses Ubuntu’s package management tools to check for available updates.

The required APT tools should already be available on most Ubuntu installations.

## Requirements

Aurora requires:

* Linux
* Python 3
* systemd
* `python-rich`

Additional requirements depend on your distribution.

For Arch Linux, you also need:

* `pacman-contrib`

## Installation

### Recommended on Arch: Install from the AUR

On Arch Linux and Arch-based distributions, the recommended way to install Aurora is through the AUR.

Using an AUR helper such as `yay`:

```bash
yay -S aurora-update-assistant
```

After installation, Aurora should install the required application files and systemd user services.

No manual systemd setup should be required.

### Manual Installation

Manual installation is mainly intended for development, testing, or non-Arch systems.

1. Clone or download the Aurora repository.
2. Place the Aurora folder in a fixed location, for example:

```bash
~/Aurora
```

3. Edit the Aurora configuration file as desired.
4. Run the manual installer:

```bash
python manual_installer.py
```

The old installer name `installer.py` is no longer used.

## Usage

Run Aurora with:

```bash
aurora
```

The main Aurora command reads the latest stored update state and reacts based on the configured thresholds. Depending on your configuration and the number of pending updates, Aurora may print status messages, warnings, recommendations, or ask whether you want to update.

To display the current update status directly, use:

```bash
aurora status
```

Example output:

```text
Aurora Status
─────────────
Severity: NONE
Updates: 2 packages
Summary: pending

Breakdown:
Details:

Recommendation:
    Critical components involved. Calm hands, clear mind.
```

## Aurora Status

The `aurora status` command gives a quick overview of the latest known update state.

It can display:

* Severity level
* Number of pending package updates
* Summary
* Breakdown
* Details
* Recommendation

This is useful when you only want to quickly check the system’s update state without going through the full Aurora assistant flow.

Because the status command reads from Aurora’s stored update state, it is fast and does not need to perform a full update check every time it runs. The stored state is updated by Aurora’s background systemd timer.

This also makes `aurora status` useful for scripts, terminal startup messages, status bars, or other tools that only need a quick update overview.

## How It Works

Aurora is made up of two main parts:

### Aurora Application

The Aurora application is the command-line program the user interacts with.

It reads the latest stored update information and displays messages based on the configured behavior. It can show whether the system is up to date, whether updates are waiting, how serious the update state is, and what action is recommended.

Depending on the configuration, Aurora can also ask whether you want to start the update process.

### Aurora Background Checker

Aurora uses a systemd service and timer to check for available updates automatically in the background.

The background checker runs the correct update-checking method for your distribution and stores the result locally. The main Aurora command can then read this result quickly instead of running a fresh package manager check every time.

This keeps Aurora lightweight while still providing recent update information.

## Configuration

Aurora can be configured to control how it reacts to available updates.

Typical configuration options may include:

* Update thresholds
* Severity levels
* Cooldown behavior
* Background check interval
* Distribution-specific update behavior

Edit the Aurora configuration file after installation to adjust the behavior to your preferences.

## Updating Aurora

### Arch / AUR

If Aurora was installed through the AUR, update it the same way as other AUR packages:

```bash
yay -Syu
```

Or rebuild only Aurora with:

```bash
yay -S aurora-update-assistant
```

### Manual Installation

For manual installations, update the local Aurora files from the repository and rerun:

```bash
python manual_installer.py
```

## Roadmap

Planned improvements include:

* Support for more Linux distributions
* Better package manager abstraction
* Improved status output
* More configurable update behavior
* Optional desktop notifications
* Better handling of critical or security-related updates

## License

Aurora is licensed under the GNU General Public License v3.
