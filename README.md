# 🌌 Galactic StarGazer
## Overview 🌟

Galactic StarGazer is a project designed to display GitHub repository statistics on the Galactic Unicorn, a display based on the Raspberry Pi Pico. It provides real-time information such as star and fork counts for specified GitHub repositories.

## Features ✨

- Real-time display of GitHub repository statistics.
- Scrolling text for detailed repository information.
- Customizable repository list and display settings.
- Wi-Fi connectivity for live data updates.
- Adjustable brightness control.

## Hardware Requirements 🦄

- Pimoroni's [Galactic Unicorn](https://shop.pimoroni.com/products/space-unicorns?variant=40842033561683) display.

## Software Dependencies 💻

- Thonny (or a similar application) for copying files to the Galactic Unicorn.

## Setup Instructions 📝

### Hardware Setup:
- Connect the Galactic Unicorn display to your computer.

### Software Installation:
- Clone the repository to your computer.
- Use Thonny or a similar application to copy the following files from the cloned repository to the Galactic Unicorn:
    - `main.py` - The main code for the project.
    - `GITHUB_TOKEN_example.py` - Rename this file to GITHUB_TOKEN.py and update it with your own GitHub access token.
    - `WIFI_CONFIG_example.py` - Rename this file to WIFI_CONFIG.py and update it with the Wi-Fi network details you want the Galactic Unicorn to connect to.
- Run the script:
    - The code contained in `main.py` will run automatically when the Galactic Unicorn is rebooted.

## Configuration ⚙️

- **Wi-Fi Configuration:** Edit `WIFI_CONFIG.py` with your Wi-Fi details (SSID and password).
- **GitHub Token:** Add your GitHub API token to `GITHUB_TOKEN.py for accessing repository data.

## Usage 🖥️

- After setup, the Galactic StarGazer will display statistics from the configured GitHub repositories.
- Use the built-in buttons on the Galactic Unicorn to adjust the brightness as needed.

## Customisation 🎨

- **Repository Selection:** Modify the repositories list in `main.py to display your desired GitHub repositories.
- **Display Settings:** Change pen colors and other settings in `main.py` to customise the look of your display.

## Troubleshooting 🔧

- **Wi-Fi Issues:** Ensure the Wi-Fi details in `WIFI_CONFIG.py` are correct.
- **API Token:** Ensure your `GITHUB_TOKEN.py` has a valid GitHub API token.

## Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licence 📜
This project is released under the [MIT](https://choosealicense.com/licenses/mit/) licence.