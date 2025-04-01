from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  # Import Service for WebDriver
from selenium.webdriver.common.action_chains import ActionChains  # Import for advanced interactions
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
        # Use the user data directory to persist the login session
        options.add_argument("--user-data-dir=/home/iedwards/.config/chromium")  # Path to Chromium user data directory
        # options.add_argument("--headless")  # Optional: Run in headless mode (no GUI)

        # Use Service to specify the WebDriver executable path
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()  # Maximize the browser window
        print("WebDriver initialized and window maximized.")
    except FileNotFoundError:
        print("Chromedriver not found at /usr/bin/chromedriver. Please install it to proceed.")
        print("Visit https://chromedriver.chromium.org/downloads to download the correct version.")
        driver = None
    except Exception as e:
        print(f"Failed to initialize WebDriver: {e}")
        print("Ensure that the Chromedriver version matches the Chromium browser version.")
        driver = None

def open_whatsapp_web():
    """
    Opens WhatsApp Web and waits until it is fully loaded.
    """
    try:
        if not driver:
            print("WebDriver is not initialized.")
            return False

        driver.get("https://web.whatsapp.com")
        print("Opening WhatsApp Web...")

        # Wait until the search box is present, indicating WhatsApp Web is loaded
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("WhatsApp Web is loaded and ready.")
        return True
    except Exception as e:
        print(f"An error occurred while opening WhatsApp Web: {e}")
        return False

# Function to send the message
def send_whatsapp_message(contact_name, message):
    """
    Sends a WhatsApp message to the specified contact.
    """
    try:
        # Search for the contact
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Scroll the chat text box into view and send the message
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", message_box)  # Scroll into view
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.RETURN)
        time.sleep(5)
        print(f"Message sent to {contact_name}!")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

def send_whatsapp_poll(contact_name, question, options):
    """
    Sends a WhatsApp poll to the specified contact.
    """
    try:
        # Search for the contact
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Locate and click the "Attach" button
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach"]'))
        )
        attach_button.click()
        time.sleep(2)

        # Select the "Poll" option
        poll_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[.//span[text()="Poll"]]'))
        )
        poll_option.click()
        time.sleep(2)

        # Locate the "Ask question" input box
        question_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Ask question"]/following-sibling::div//div[@contenteditable="true"]'))
        )
        question_box.click()
        question_box.send_keys(question)
        time.sleep(2)

        # Fill in the poll options
        for i in range(2, len(options) + 2):
            option_box = driver.find_element(By.XPATH, f'(//div[@contenteditable="true"])[{i}]')
            option_box.click()
            option_box.send_keys(options[i-2])
            time.sleep(2)

        # Send the poll
        send_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Send"]')
        send_button.click()
        time.sleep(5)
        print(f"Poll sent to {contact_name}!")
    except Exception as e:
        print(f"An error occurred while sending the poll: {e}")

# Start the WebDriver in a separate thread
def start_driver_thread():
    driver_thread = threading.Thread(target=init_driver)
    driver_thread.start()
    driver_thread.join()  # Wait for the WebDriver to initialize

if __name__ == "__main__":
    # Start the WebDriver in a separate thread
    start_driver_thread()
    time.sleep(2)
    # Example usage: send a message immediately
    if driver:
        if open_whatsapp_web():
            send_whatsapp_message("CONTACT NAME", "Hello! This is a test message.")
            # print("Message sent!")

            # Example usage: send a poll
            send_whatsapp_poll(
                "CONTACT NAME",
                "What is your favorite programming language?",
                ["Python", "JavaScript", "C++", "Java"]
            )
            print("Poll sent!")

            # Quit the driver after sending the message and poll
            # driver.quit()
    else:
        print("WebDriver was not initialized. Exiting.")