import time
import os
import platform
import pickle
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from colorama import init, Fore, Style
import pyfiglet
import pyautogui
import cv2
import numpy as np
import requests
import random
from fake_useragent import UserAgent
from undetected_chromedriver import Chrome as UndetectedChrome
from undetected_chromedriver import ChromeOptions as UndetectedChromeOptions

# Initialize colorama
init(autoreset=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        logging.error(f"Error fetching IP address: {e}")
        return None

# Get and log public IP address
public_ip = get_public_ip()
if public_ip:
    print(f"Public IP Address: {public_ip}")
    logging.info(f"Public IP Address: {public_ip}")
else:
    print("Could not fetch public IP address.")
    logging.error("Could not fetch public IP address.")

hello_world_banner = pyfiglet.figlet_format("Hello World", font="slant")
ascii_banner = pyfiglet.figlet_format("Talaat Sami", font="slant")

print(Fore.RED + Style.BRIGHT + hello_world_banner)
print(Fore.GREEN + Style.BRIGHT + ascii_banner)

# Check system type
system = platform.system()

# Initialize UserAgent
ua = UserAgent()

# Function to initialize browser options
def get_browser_options(browser_name, proxy=None):
    user_agent = ua.random
    # proxy = "http://your_proxy:your_port"  # Replace with your proxy

    if browser_name == "chrome":
        options = UndetectedChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument(f"user-agent={user_agent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")  # Uncomment to enable proxy
        return options
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.set_preference("general.useragent.override", user_agent)
        if proxy:
            # options.set_preference("network.proxy.type", 1)  # Uncomment to enable proxy
            # options.set_preference("network.proxy.http", "your_proxy")  # Uncomment to enable proxy
            # options.set_preference("network.proxy.http_port", your_port)  # Uncomment to enable proxy
            # options.set_preference("network.proxy.ssl", "your_proxy")  # Uncomment to enable proxy
            # options.set_preference("network.proxy.ssl_port", your_port)  # Uncomment to enable proxy
            pass
        return options
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--inprivate")
        options.add_argument(f"user-agent={user_agent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")  # Uncomment to enable proxy
        return options
    elif browser_name == "brave":
        options = ChromeOptions()
        brave_path = r"C:\Users\\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.binary_location = brave_path
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument(f"user-agent={user_agent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")  # Uncomment to enable proxy
        return options
    elif browser_name == "tor":
        options = ChromeOptions()
        tor_path = r"C:\Users\\Downloads\Tor Browser\Browser\firefox.exe"  # Replace with your Tor Browser executable path
        options.binary_location = tor_path
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument(f"user-agent={user_agent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")  # Uncomment to enable proxy
        return options
    else:
        raise ValueError("Unsupported browser")

# Function to initialize driver for the selected browser
def get_driver(browser_name, options=None):
    if browser_name == "chrome":
        return UndetectedChrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser_name == "firefox":
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    elif browser_name == "edge":
        return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    elif browser_name == "brave":
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser_name == "tor":
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError("Unsupported browser")

def print_colored(text, color):
    if color == 'red':
        print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)
    elif color == 'green':
        print(Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL)
    elif color == 'blue':
        print(Fore.BLUE + Style.BRIGHT + text + Style.RESET_ALL)
    elif color == 'white':
        print(Fore.WHITE + Style.BRIGHT + text + Style.RESET_ALL)
    elif color == 'cyan':
        print(Fore.CYAN + Style.BRIGHT + text + Style.RESET_ALL)
    elif color == 'magenta':
        print(Fore.MAGENTA + Style.BRIGHT + text + Style.RESET_ALL)
    else:
        print(text + Style.RESET_ALL)  # If no valid color, print text without color

# Function to choose a browser (including Tor)
def choose_browser():
    while True:
        print_colored("Choose a browser to launch:", 'cyan')
        print_colored("1. Chrome", 'green')
        print_colored("2. Firefox", 'blue')
        print_colored("3. Edge", 'white')
        print_colored("4. Brave", 'magenta')
        print_colored("5. Tor", 'red')

        choice = input("Enter the number of the browser: ")

        if choice == "1":
            return "chrome"
        elif choice == "2":
            return "firefox"
        elif choice == "3":
            return "edge"
        elif choice == "4":
            return "brave"
        elif choice == "5":
            return "tor"
        else:
            print("Invalid choice. Please enter a valid number.")

# Get user's browser choice
browser_choice = choose_browser()

try:
    if browser_choice == "tor":
        # Launch Tor Browser
        driver = get_driver(browser_choice, options=get_browser_options(browser_choice))
        logging.info("Tor Browser launched")
        
    else:
        # Launch the selected browser
        driver = get_driver(browser_choice, options=get_browser_options(browser_choice))
        logging.info(f"{browser_choice.capitalize()} browser launched")

    driver.get("https://nowsecure.nl")
    logging.info(f"Website accessed in {browser_choice.capitalize()} browser")

    # Save the driver instance for later use
    drivers = [driver]

except ValueError as e:
    logging.error(f"Unsupported browser choice: {browser_choice}")
    exit(1)
except Exception as e:
    logging.error(f"Error launching {browser_choice.capitalize()} browser: {e}")
    exit(1)

# Function to click a button using a reference image
def find_button_and_click(button_image_path):
    try:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        button_image = cv2.imread(button_image_path)

        result = cv2.matchTemplate(screenshot_np, button_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.8:  # Ensure accuracy of the match
            pyautogui.click(max_loc[0], max_loc[1])
        else:
            logging.error("Button not found")
    except Exception as e:
        logging.error(f"Error finding and clicking button: {e}")

# Coordinates for the install button (you can replace this step with an image)
install_button_coordinates = (100, 100)  # Set correct coordinates for the install button
try:
    pyautogui.click(install_button_coordinates[0], install_button_coordinates[1])
    logging.info("Clicked install button")
except Exception as e:
    logging.error(f"Error clicking install button: {e}")

# Wait for the extension to install
time.sleep(5)

# Save cookies
def save_cookies(driver, path):
    try:
        with open(path, 'wb') as filehandler:
            pickle.dump(driver.get_cookies(), filehandler)
    except Exception as e:
        logging.error(f"Error saving cookies: {e}")

def load_cookies(driver, path):
    try:
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except Exception as e:
        logging.error(f"Error loading cookies: {e}")

for driver in drivers:
    save_cookies(driver, "cookies.pkl")

options = get_browser_options(browser_choice)
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument(f"user-agent={ua.random}")

driver = get_driver(browser_choice)
driver.get("https://www.example.com")

def get_browser_options(browser_name, proxy=None):
    user_agent = ua.random
    if browser_name == "chrome":
        options = UndetectedChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument(f"user-agent={user_agent}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        return options
    # ...

# List of proxies
#proxies = [
  #  "http://123.456.789.012:8080",
  #  "http://987.654.321.098:8080",
    # ...
#]

# Open a new tab for each proxy
#for proxy in proxies:
   # options = get_browser_options(browser_choice, proxy)
  #  driver = get_driver(browser_choice, options)
  #  driver.get("https://www.example.com")
   # drivers.append(driver)

try:
    result = 10 / 0  # This will raise a ZeroDivisionError
except ZeroDivisionError as e:
    logging.error(f"Error occurred: {e}")
    # Handle the error in a way that fits your application logic
except Exception as e:
    logging.error(f"Unexpected error occurred: {e}")
finally:
    logging.info("Execution completed")

try:
    while True:
        time.sleep(random.uniform(1, 5))
except KeyboardInterrupt:
    for driver in drivers:
        driver.quit()
    logging.info("Browsers closed")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    for driver in drivers:
        driver.quit()
    logging.info("Browsers closed due to an error")

time.sleep(8000)
logging.info("Program completed its run.")
print("Program continues to run...")
