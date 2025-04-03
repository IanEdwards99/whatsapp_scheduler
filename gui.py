import tkinter as tk
from tkinter import messagebox
from whatsapp_scheduler.scheduler import MessageScheduler
from whatsapp_scheduler.web_driver import WebDriverManager
from whatsapp_scheduler.whatsapp import WhatsApp

class WhatsAppSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Scheduler")
        self.scheduler = MessageScheduler("schedules/schedule.json")

        # Contact
        tk.Label(root, text="Contact Name:").grid(row=0, column=0, padx=10, pady=5)
        self.contact_entry = tk.Entry(root, width=30)
        self.contact_entry.grid(row=0, column=1, padx=10, pady=5)

        # Message
        tk.Label(root, text="Message:").grid(row=1, column=0, padx=10, pady=5)
        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.grid(row=1, column=1, padx=10, pady=5)

        # Poll Question
        tk.Label(root, text="Poll Question:").grid(row=2, column=0, padx=10, pady=5)
        self.poll_question_entry = tk.Entry(root, width=30)
        self.poll_question_entry.grid(row=2, column=1, padx=10, pady=5)

        # Poll Options
        tk.Label(root, text="Poll Options (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
        self.poll_options_entry = tk.Entry(root, width=30)
        self.poll_options_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Send Message Now", command=self.send_message_now).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(root, text="Send Poll Now", command=self.send_poll_now).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(root, text="Schedule Message", command=self.schedule_message).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(root, text="Schedule Poll", command=self.schedule_poll).grid(row=5, column=1, padx=10, pady=10)
        tk.Button(root, text="List Schedules", command=self.list_schedules).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(root, text="Quit", command=root.quit).grid(row=6, column=1, padx=10, pady=10)

    def send_message_now(self):
        contact = self.contact_entry.get()
        message = self.message_entry.get()
        if not contact or not message:
            messagebox.showerror("Error", "Please provide both contact and message.")
            return

        driver_manager = WebDriverManager()
        driver_manager.start_driver_thread()
        driver = driver_manager.get_driver()

        if driver:
            whatsapp = WhatsApp(driver)
            if whatsapp.open_whatsapp_web():
                whatsapp.send_message(contact, message)
                messagebox.showinfo("Success", "Message sent successfully!")
            driver.quit()
        else:
            messagebox.showerror("Error", "Failed to initialize WebDriver.")

    def send_poll_now(self):
        contact = self.contact_entry.get()
        question = self.poll_question_entry.get()
        options = self.poll_options_entry.get().split(",")
        if not contact or not question or not options:
            messagebox.showerror("Error", "Please provide contact, question, and options.")
            return

        driver_manager = WebDriverManager()
        driver_manager.start_driver_thread()
        driver = driver_manager.get_driver()

        if driver:
            whatsapp = WhatsApp(driver)
            if whatsapp.open_whatsapp_web():
                whatsapp.send_poll(contact, question, options)
                messagebox.showinfo("Success", "Poll sent successfully!")
            driver.quit()
        else:
            messagebox.showerror("Error", "Failed to initialize WebDriver.")

    def schedule_message(self):
        contact = self.contact_entry.get()
        message = self.message_entry.get()
        time = tk.simpledialog.askstring("Schedule Time", "Enter time (DD/MM/YYYY HH:MM):")
        if not contact or not message or not time:
            messagebox.showerror("Error", "Please provide contact, message, and time.")
            return
        self.scheduler.add_message_schedule(contact, message, time, None)
        messagebox.showinfo("Success", "Message scheduled successfully!")

    def schedule_poll(self):
        contact = self.contact_entry.get()
        question = self.poll_question_entry.get()
        options = self.poll_options_entry.get().split(",")
        time = tk.simpledialog.askstring("Schedule Time", "Enter time (DD/MM/YYYY HH:MM):")
        if not contact or not question or not options or not time:
            messagebox.showerror("Error", "Please provide contact, question, options, and time.")
            return
        if len(options) != len(set(options)):
            messagebox.showerror("Error", "Poll options must be unique. Please provide distinct options.")
            return
        self.scheduler.add_poll_schedule(contact, question, options, time, None)
        messagebox.showinfo("Success", "Poll scheduled successfully!")

    def list_schedules(self):
        schedules = self.scheduler.list_schedules()
        if schedules:
            schedule_list = "\n".join([f"{i}: {schedule}" for i, schedule in enumerate(schedules)])
            messagebox.showinfo("Schedules", schedule_list)
        else:
            messagebox.showinfo("Schedules", "No schedules found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppSchedulerGUI(root)
    root.mainloop()
