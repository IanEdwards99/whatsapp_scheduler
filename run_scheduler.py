import time
from datetime import datetime
from whatsapp_scheduler.web_driver import WebDriverManager
from whatsapp_scheduler.whatsapp import WhatsApp
from whatsapp_scheduler.scheduler import MessageScheduler

def run_scheduler():
    scheduler = MessageScheduler("schedules/schedule.json")
    driver_manager = WebDriverManager()
    driver_manager.start_driver_thread()
    driver = driver_manager.get_driver()

    if not driver:
        print("WebDriver initialization failed. Exiting.")
        return

    whatsapp = WhatsApp(driver)

    if not whatsapp.open_whatsapp_web():
        print("Failed to open WhatsApp Web. Exiting.")
        driver.quit()
        return

    while True:
        now = datetime.now()
        schedules = scheduler.get_due_schedules(now)

        for schedule in schedules:
            if schedule["type"] == "message":
                whatsapp.send_message(schedule["contact"], schedule["message"])
            elif schedule["type"] == "poll":
                whatsapp.send_poll(schedule["contact"], schedule["question"], schedule["options"])

            scheduler.mark_as_sent(schedule)

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_scheduler()