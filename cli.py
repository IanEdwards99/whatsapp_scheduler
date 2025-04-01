import argparse
from whatsapp_scheduler.scheduler import MessageScheduler

def main():
    parser = argparse.ArgumentParser(description="WhatsApp Scheduler CLI")
    parser.add_argument("action", choices=["add", "modify", "list", "delete"], help="Action to perform")
    parser.add_argument("--type", choices=["message", "poll"], required=True, help="Type of schedule (message or poll)")
    parser.add_argument("--contact", help="Contact name")
    parser.add_argument("--message", help="Message to send (for messages)")
    parser.add_argument("--question", help="Poll question (for polls)")
    parser.add_argument("--options", nargs="+", help="Poll options (for polls)")
    parser.add_argument("--time", required=True, help="Time to send the schedule (DD/MM/YYYY HH:MM)")
    parser.add_argument("--recurring", choices=["daily", "weekly", "monthly"], help="Set as recurring schedule")

    args = parser.parse_args()
    scheduler = MessageScheduler("schedules/schedule.json")

    if args.action == "add":
        if args.type == "message":
            if args.contact and args.message:
                scheduler.add_message_schedule(args.contact, args.message, args.time, args.recurring)
                print("Message schedule added.")
            else:
                print("Missing required arguments for adding a message schedule.")
        elif args.type == "poll":
            if args.contact and args.question and args.options:
                scheduler.add_poll_schedule(args.contact, args.question, args.options, args.time, args.recurring)
                print("Poll schedule added.")
            else:
                print("Missing required arguments for adding a poll schedule.")
    elif args.action == "list":
        schedules = scheduler.list_schedules()
        if schedules:
            for i, schedule in enumerate(schedules):
                print(f"{i}: {schedule}")
        else:
            print("No schedules found.")
    elif args.action == "delete":
        if args.contact:
            scheduler.remove_schedule(int(args.contact))
            print("Schedule deleted.")
        else:
            print("Missing required arguments for deleting a schedule.")

if __name__ == "__main__":
    main()