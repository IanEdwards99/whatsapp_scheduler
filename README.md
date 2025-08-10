# WhatsApp Scheduler

WhatsApp Scheduler is a Python-based tool that allows you to schedule and send WhatsApp messages or polls. It provides three interfaces for interaction:
1. **Flask Web App**: A user-friendly web interface.
2. **Python GUI**: A desktop-based graphical interface using `tkinter`.
3. **Python CLI**: A command-line interface for advanced users.

The tool also includes a background scheduler (`run_scheduler.py`) to automatically send scheduled messages and polls.

---

## Setup

### Prerequisites
1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Chromium and Chromedriver**: Install Chromium and Chromedriver for Selenium.
   - On Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install chromium-browser chromium-chromedriver
     ```
3. **Install Dependencies**:
   - Use `pip` to install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

### Repository Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/whatsapp_scheduler.git
   cd whatsapp_scheduler
   ```
2. Create a directory for schedules:
   ```bash
   mkdir schedules
   ```
3. Create an empty schedule file:
   ```bash
   touch schedules/schedule.json
   ```

---

## Usage

### 1. Flask Web App
The Flask web app provides a user-friendly interface to manage schedules and send messages/polls.

#### Steps to Run:
1. Start the Flask app:
   ```bash
   python3 app.py
   ```
2. Open your browser and navigate to:
   ```
   http://<your-ip>:5000
   ```
   Replace `<your-ip>` with your machine's IP address.

#### Features:
- **Home**: View all scheduled messages and polls.
- **Add Schedule**: Schedule a message or poll.
- **Send Now**: Instantly send a message or poll.
- **Undo Delete**: Undo the deletion of a schedule.

---

### 2. Python GUI
The Python GUI provides a desktop-based interface for managing schedules and sending messages/polls.

#### Steps to Run:
1. Start the GUI:
   ```bash
   python3 gui.py
   ```

#### Features:
- **Send Message Now**: Instantly send a message.
- **Send Poll Now**: Instantly send a poll.
- **Schedule Message**: Schedule a message to be sent later.
- **Schedule Poll**: Schedule a poll to be sent later.
- **List Schedules**: View all scheduled messages and polls.

---

### 3. Python CLI
The Python CLI is a command-line interface for advanced users.

#### Steps to Run:
1. Start the CLI:
   ```bash
   python3 cli.py <action> --type <type> --contact <contact> [other options]
   ```

#### Actions:
- **add**: Add a new schedule.
- **list**: List all schedules.
- **delete**: Delete a schedule.
- **send_now**: Instantly send a message or poll.

#### Example:
```bash
python3 cli.py add --type message --contact "John Doe" --message "Hello!" --time "25/12/2023 10:00"
```

---

### 4. Background Scheduler
The `run_scheduler.py` script runs in the background to automatically send scheduled messages and polls.

#### Steps to Run:
1. Start the scheduler:
   ```bash
   python3 run_scheduler.py
   ```

#### How It Works:
- The scheduler continuously checks the `schedules/schedule.json` file for due messages or polls.
- When a schedule is due, it sends the message or poll using Selenium.

---

## Notes
- Ensure that WhatsApp Web is logged in on the browser used by Selenium.
- The `schedules/schedule.json` file is used to store all scheduled tasks.
- The Flask app, GUI, and CLI all interact with the same schedule file, ensuring consistency.

---

## Troubleshooting
- **WebDriver Initialization Failed**: Ensure that Chromium and Chromedriver are installed and compatible.
- **Flask App Not Accessible**: Check if the Flask app is running on the correct IP and port.
- **Background Scheduler Not Sending Messages**: Verify that the `schedules/schedule.json` file contains valid schedules.

---

## License
This project is licensed under the MIT License.