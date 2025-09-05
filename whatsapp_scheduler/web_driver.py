from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import threading

class WebDriverManager:
    def __init__(self, binary_location="/usr/bin/chromium-browser", driver_path="/usr/bin/chromedriver"):
        self.binary_location = binary_location
        self.driver_path = driver_path
        self.driver = None

    def init_driver(self):
        try:
            options = webdriver.ChromeOptions()
            options.binary_location = self.binary_location
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-extensions")
            options.add_argument("--user-data-dir=/home/iedwards/.config/chromium")
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            print("WebDriver initialized and window maximized.")
        except Exception as e:
            print(f"Failed to initialize WebDriver: {e}")
            self.driver = None

    def start_driver_thread(self):
        driver_thread = threading.Thread(target=self.init_driver)
        driver_thread.start()
        driver_thread.join()

    def get_driver(self):
        return self.driver
