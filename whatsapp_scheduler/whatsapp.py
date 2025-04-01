from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WhatsApp:
    def __init__(self, driver):
        self.driver = driver

    def open_whatsapp_web(self):
        try:
            self.driver.get("https://web.whatsapp.com")
            print("Opening WhatsApp Web...")
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("WhatsApp Web is loaded and ready.")
            return True
        except Exception as e:
            print(f"An error occurred while opening WhatsApp Web: {e}")
            return False

    def send_message(self, contact_name, message):
        try:
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.send_keys(contact_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            message_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            message_box.click()
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            time.sleep(5)
            print(f"Message sent to {contact_name}!")
        except Exception as e:
            print(f"An error occurred while sending the message: {e}")

    def send_poll(self, contact_name, question, options):
        try:
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            search_box.send_keys(contact_name)
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
            attach_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach"]'))
            )
            attach_button.click()
            time.sleep(2)
            poll_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//li[.//span[text()="Poll"]]'))
            )
            poll_option.click()
            time.sleep(2)
            question_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Ask question"]/following-sibling::div//div[@contenteditable="true"]'))
            )
            question_box.click()
            question_box.send_keys(question)
            time.sleep(2)
            for i in range(2, len(options) + 2):
                option_box = self.driver.find_element(By.XPATH, f'(//div[@contenteditable="true"])[{i}]')
                option_box.click()
                option_box.send_keys(options[i-2])
                time.sleep(2)
            send_button = self.driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Send"]')
            send_button.click()
            time.sleep(5)
            print(f"Poll sent to {contact_name}!")
        except Exception as e:
            print(f"An error occurred while sending the poll: {e}")
