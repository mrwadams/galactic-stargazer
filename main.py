# github_repo_stats.py

import time
import uasyncio
import urequests
import json
from time import sleep
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
from network_manager import NetworkManager
import WIFI_CONFIG
import GITHUB_TOKEN

#---------- Constants & Configuration ----------#

# Setup graphics
gu = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

# Setup GitHub authentication
github_token = GITHUB_TOKEN.token

headers = {
    'Authorization': f'token {github_token}',
    'User-Agent': 'GalacticRepoStats'
}

# Mapping dictionary for repo names
repo_name_map = {
    'mrwadams/stride-gpt': 'STRIDE GPT',
    'mrwadams/attackgen': 'AttackGen',
    'mrwadams/takedown-gpt': 'Takedown GPT'
}

# List of repositories
repositories = list(repo_name_map.keys())

# Define pen colors
BLACK = graphics.create_pen(0, 0, 0)
WHITE = graphics.create_pen(255, 255, 255)
REPO_NAME_COLOR = graphics.create_pen(102, 255, 102)  # Green color for repository name
STATS_COLOR = graphics.create_pen(255, 255, 255)  # White color for stats

# Scrolling text setup
PADDING = 5
MESSAGE_COLOUR = (255, 255, 255)
OUTLINE_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (0, 0, 153)
HOLD_TIME = 2.0  # Time to hold the message at the start and end
STEP_TIME = 0.075  # Time per step for scrolling

# State constants
STATE_PRE_SCROLL = 0
STATE_SCROLLING = 1
STATE_POST_SCROLL = 2

shift = 0
state = STATE_PRE_SCROLL

# Set font and brightness (adjust as needed)
graphics.set_font("bitmap8")
gu.set_brightness(0.5)

#---------- Function Definitions ----------#

def status_handler(mode, status, ip):
    # Reports Wi-Fi connection status
    print(mode, status, ip)
    print('Connecting to Wi-Fi...')
    if status is not None:
        if status:
            print('Wi-Fi connection successful!')
        else:
            print('Wi-Fi connection failed!')

def outline_text(repo_name, stats, x, y):
    # Render the repository name with outline
    repo_name_x = x
    graphics.set_pen(BLACK)  # Outline color
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:  # Skip the center position for the outline
                graphics.text(repo_name, repo_name_x + dx, y + dy, -1, 1)
    
    graphics.set_pen(REPO_NAME_COLOR)
    graphics.text(repo_name, repo_name_x, y, -1, 1)

    # Calculate the x position for stats based on repo name width
    stats_x = repo_name_x + graphics.measure_text(repo_name, 1)

    # Render the stats text with outline
    graphics.set_pen(BLACK)  # Outline color
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:  # Skip the center position for the outline
                graphics.text(stats, stats_x + dx, y + dy, -1, 1)
    
    graphics.set_pen(STATS_COLOR)
    graphics.text(stats, stats_x, y, -1, 1)



#---------- Networking Setup ----------#

wifi_connected = False
try:
    network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
    wifi_connected = True
except Exception as e:
    print(f'Wi-Fi connection failed! {e}')


#---------- Main Loop ----------#

while wifi_connected:
    for repo in repositories:
        try:
            response = urequests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            print(f"Status Code for {repo}: {response.status_code}")

            if response.status_code == 200:
                repo_data = json.loads(response.text)
                # Split display text into repo name and stats
                display_name = repo_name_map.get(repo, "Unknown Repo")
                stars = repo_data['stargazers_count']
                forks = repo_data['forks_count']
                repo_name_text = f"{display_name} - "
                stats_text = f"Stars : {stars}   Forks : {forks}"
                msg_width = graphics.measure_text(f"{repo_name_text}{stats_text}", 1)

                # Scrolling logic
                last_time = time.ticks_ms()
                shift = 0
                state = STATE_PRE_SCROLL

                while True:
                    time_ms = time.ticks_ms()
                    
                    # Brightness control integration
                    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
                        gu.adjust_brightness(+0.01)

                    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
                        gu.adjust_brightness(-0.01)

                    if state == STATE_PRE_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
                        if msg_width + PADDING * 2 >= width:
                            state = STATE_SCROLLING
                        last_time = time_ms

                    if state == STATE_SCROLLING and time_ms - last_time > STEP_TIME * 1000:
                        shift += 1
                        if shift >= msg_width + PADDING * 2 - width - 1:
                            state = STATE_POST_SCROLL
                        last_time = time_ms

                    if state == STATE_POST_SCROLL and time_ms - last_time > HOLD_TIME * 1000:
                        break  # Exit the while loop after scrolling is complete

                    # Draw the text
                    graphics.set_pen(graphics.create_pen(int(BACKGROUND_COLOUR[0]), int(BACKGROUND_COLOUR[1]), int(BACKGROUND_COLOUR[2])))
                    graphics.clear()
                    # Call the modified outline_text function
                    outline_text(repo_name_text, stats_text, x=PADDING - shift, y=2)
                    gu.update(graphics)

                    # Pause to prevent USB serial device failure
                    time.sleep(0.001)

            else:
                print(f"Failed to fetch data for {repo}. Status Code: {response.status_code}")

            response.close()

        except Exception as e:
            print(f"Error: {e}")

        sleep(5)  # Short pause between repositories

    sleep(5)  # Short pause after all repositories have been displayed
