import argparse
from whatsapp_scheduler.scheduler import MessageScheduler
from whatsapp_scheduler.web_driver import WebDriverManager
from whatsapp_scheduler.whatsapp import WhatsApp

def main():
    parser = argparse.ArgumentParser(description="WhatsApp Scheduler CLI")
    parser.add_argument("action", choices=["add", "modify", "list", "delete", "send_now"], help="Action to perform")
    parser.add_argument("--type", choices=["message", "poll"], required=True, help="Type of schedule (message or poll)")

    # Common arguments
    parser.add_argument("--contact", required=True, help="Contact name (required for both messages and polls)")
    parser.add_argument("--time", help="Time to send the schedule (DD/MM/YYYY HH:MM)")
    parser.add_argument("--recurring", choices=["daily", "weekly", "monthly"], help="Set as recurring schedule")

    # Group arguments for messages
    message_args = parser.add_argument_group("Message Arguments", "Arguments specific to sending messages")
    message_args.add_argument("--message", help="Message to send (required for messages)")

    # Group arguments for polls
    poll_args = parser.add_argument_group("Poll Arguments", "Arguments specific to sending polls")
    poll_args.add_argument("--question", help="Poll question (required for polls)")
    poll_args.add_argument("--options", nargs="+", help="Poll options (required for polls)")

    args = parser.parse_args()

    if args.action == "send_now":
        if args.contact:
            if args.type == "message":
                if args.message:
                    driver_manager = WebDriverManager()
                    driver_manager.start_driver_thread()
                    driver = driver_manager.get_driver()

                    if driver:
                        whatsapp = WhatsApp(driver)
                        if whatsapp.open_whatsapp_web():
                            whatsapp.send_message(args.contact, args.message)
                            print("Message sent immediately.")
                        driver.quit()
                    else:
                        print("Failed to initialize WebDriver.")
                else:
                    print("Please include a message to send.")
            elif args.type == "poll":
                if args.question and args.options:
                    driver_manager = WebDriverManager()
                    driver_manager.start_driver_thread()
                    driver = driver_manager.get_driver()

                    if driver:
                        whatsapp = WhatsApp(driver)
                        if whatsapp.open_whatsapp_web():
                            whatsapp.send_poll(args.contact, args.question, args.options)
                            print("Poll sent immediately.")
                        driver.quit()
                    else:
                        print("Failed to initialize WebDriver.")
                else:
                    print("Please ensure both a `question` and `options` are specified.")
        else:
            print("Please specify a contact to send message/poll to.")
    elif args.action == "add":
        scheduler = MessageScheduler("schedules/schedule.json")
        if args.contact:
            if args.type == "message":
                if args.message and args.time:
                    scheduler.add_message_schedule(args.contact, args.message, args.time, args.recurring)
                    print("Message schedule added.")
                else:
                    print("Please ensure a `message` and a `time` is specified for the scheduled message.")
            elif args.type == "poll":
                if args.question and args.options and args.time:
                    if len(args.options) != len(set(args.options)):
                        print("Poll options must be unique. Please provide distinct options.")
                        return
                    scheduler.add_poll_schedule(args.contact, args.question, args.options, args.time, args.recurring)
                    print("Poll schedule added.")
                else:
                    print("Please ensure a `question`, `options`, and `time` are specified for the scheduled poll.")
        else:
            print("Please specify a contact to schedule a message/poll for.")
    elif args.action == "list":
        schedules = scheduler.list_schedules()
        if schedules:
            for i, schedule in enumerate(schedules):
                print(f"{i}: {schedule}")
        else:
            print("No schedules found.")
    elif args.action == "delete":
        scheduler = MessageScheduler("schedules/schedule.json")
        schedules = scheduler.list_schedules()
        if schedules:
            print("Here are the current schedules:")
            for i, schedule in enumerate(schedules):
                print(f"{i}: {schedule}")
            try:
                index = int(input("Enter the index of the schedule to delete: "))
                if 0 <= index < len(schedules):
                    scheduler.remove_schedule(index)
                    print("Schedule deleted.")
                else:
                    print("Invalid index. No schedule deleted.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("No schedules found to delete.")

if __name__ == "__main__":
    main()