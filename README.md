# Windows Set Theme

This project provides scripts to automatically switch Windows themes based on the time of day, changing between light and dark themes. It includes both Python and Rust implementations.

## Features

When it runs:
- Switches to the light theme during the day.
- Switches to the dark theme during the night.
- Configures both `SystemUsesLightTheme` and `AppsUseLightTheme` registry settings.

## How It Works

Both implementations determine whether it is daytime or nighttime based on the system's current time:
- **Daytime:** 8:00 AM to 6:00 PM
- **Nighttime:** All other times

Based on the current time, the script updates the Windows registry to set the appropriate theme and restarts the explorer to apply the changes.

## Running the Script

### Python

To run the Python script:

```sh
python set_theme.py
```

### Rust

To build and run the Rust project:

```sh
# Build the project
cd rust
cargo build --release

# Run the executable:
./target/release/windows_set_theme
```