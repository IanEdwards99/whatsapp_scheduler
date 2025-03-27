from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # Import Service for WebDriver
from selenium.webdriver.support.ui import WebDriverWait  # Import for explicit waits
from selenium.webdriver.support import expected_conditions as EC  # Import for wait conditions
import time
import threading

# Global variable for the WebDriver
driver = None

# Initialize WebDriver for Chromium
def init_driver():
    global driver
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"  # Specify the Chromium binary location
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")  # Disable GPU acceleration for better performance
        options.add_argument("--user-data-dir=/home/iedwards/.config/chromium")  # Path to Chromium user data directory

        # Use Service to specify the WebDriver executable path
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()  # Maximize the browser window
        print("WebDriver initialized and window maximized.")
    except FileNotFoundError:
        print("Chromedriver not found at /usr/bin/chromedriver. Please install it to proceed.")
        driver = None
    except Exception as e:
        print(f"Failed to initialize WebDriver: {e}")
        driver = None

# Start the WebDriver in a separate thread
def start_driver_thread():
    driver_thread = threading.Thread(target=init_driver)
    driver_thread.start()
    driver_thread.join()  # Wait for the WebDriver to initialize

if __name__ == "__main__":
    # Start the WebDriver in a separate thread
    start_driver_thread()

    # Keep the script running to allow manual interaction
    print("WebDriver is ready. You can now interact with it manually.")
    print("Use the 'driver' object to execute commands.")
    print("For example:")
    print("  driver.get('https://web.whatsapp.com')")
    print("  # Then manually locate and interact with elements.")
    print("Press Ctrl+D to exit.")