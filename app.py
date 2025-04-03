from flask import Flask, render_template, request, redirect, url_for, flash, session
from whatsapp_scheduler.scheduler import MessageScheduler
from whatsapp_scheduler.web_driver import WebDriverManager
from whatsapp_scheduler.whatsapp import WhatsApp

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key
scheduler = MessageScheduler("schedules/schedule.json")

@app.route("/")
def index():
    schedules = scheduler.list_schedules()
    return render_template("index.html", schedules=schedules, enumerate=enumerate)

@app.route("/add", methods=["GET", "POST"])
def add_schedule():
    if request.method == "POST":
        schedule_type = request.form.get("type")
        contact = request.form.get("contact")
        time = request.form.get("time")
        recurring = request.form.get("recurring")
        
        if schedule_type == "message":
            message = request.form.get("message")
            if not contact or not message or not time:
                flash("Please provide contact, message, and time.", "error")
                return redirect(url_for("add_schedule"))
            scheduler.add_message_schedule(contact, message, time, recurring)
            flash("Message schedule added successfully!", "success")
        elif schedule_type == "poll":
            question = request.form.get("question")
            options = request.form.get("options").split(",")
            if not contact or not question or not options or not time:
                flash("Please provide contact, question, options, and time.", "error")
                return redirect(url_for("add_schedule"))
            if len(options) != len(set(options)):
                flash("Poll options must be unique.", "error")
                return redirect(url_for("add_schedule"))
            scheduler.add_poll_schedule(contact, question, options, time, recurring)
            flash("Poll schedule added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_schedule.html")

@app.route("/delete/<int:index>")
def delete_schedule(index):
    schedules = scheduler.list_schedules()
    if 0 <= index < len(schedules):
        deleted_schedule = schedules[index]
        scheduler.remove_schedule(index)
        session["deleted_schedule"] = deleted_schedule
        flash("Schedule deleted successfully! <a href='/undo_delete'>Undo</a>", "success")
    else:
        flash("Invalid schedule index.", "error")
    return redirect(url_for("index"))

@app.route("/undo_delete")
def undo_delete():
    deleted_schedule = session.pop("deleted_schedule", None)
    if deleted_schedule:
        scheduler.schedules.append(deleted_schedule)
        scheduler.save_schedules()
        flash("Deletion undone. Schedule restored.", "success")
    else:
        flash("No schedule to undo.", "error")
    return redirect(url_for("index"))

@app.route("/send_now", methods=["GET", "POST"])
def send_now():
    if request.method == "POST":
        schedule_type = request.form.get("type")
        contact = request.form.get("contact")

        if schedule_type == "message":
            message = request.form.get("message")
            if not contact or not message:
                flash("Please provide contact and message.", "error")
                return redirect(url_for("send_now"))
            driver_manager = WebDriverManager()
            driver_manager.start_driver_thread()
            driver = driver_manager.get_driver()
            if driver:
                whatsapp = WhatsApp(driver)
                if whatsapp.open_whatsapp_web():
                    whatsapp.send_message(contact, message)
                    flash("Message sent successfully!", "success")
                driver.quit()
            else:
                flash("Failed to initialize WebDriver.", "error")
        elif schedule_type == "poll":
            question = request.form.get("question")
            options = request.form.get("options").split(",")
            if not contact or not question or not options:
                flash("Please provide contact, question, and options.", "error")
                return redirect(url_for("send_now"))
            if len(options) != len(set(options)):
                flash("Poll options must be unique.", "error")
                return redirect(url_for("send_now"))
            driver_manager = WebDriverManager()
            driver_manager.start_driver_thread()
            driver = driver_manager.get_driver()
            if driver:
                whatsapp = WhatsApp(driver)
                if whatsapp.open_whatsapp_web():
                    whatsapp.send_poll(contact, question, options)
                    flash("Poll sent successfully!", "success")
                driver.quit()
            else:
                flash("Failed to initialize WebDriver.", "error")
        return redirect(url_for("index"))
    return render_template("send_now.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
