import os
import subprocess
import json
from datetime import datetime
import sqlite3
from llm_utils import query_llm

DATA_DIR = "/data"

def execute_task(task):
    if "install uv" in task and "datagen.py" in task:
        email = task.split()[-1]
        if not subprocess.run(["which", "uv"], capture_output=True).stdout.strip():
            subprocess.run(["uv", "pip", "install", "uv"], check=True)
        subprocess.run(["python3", "datagen.py", email], check=True)
        return "/data/generated_files/"

    elif "format" in task and "prettier" in task:
        subprocess.run(["npx", "prettier", "--write", "/data/format.md"], check=True)
        return "/data/format.md"

    elif "count" in task and "Wednesdays" in task:
        with open(f"{DATA_DIR}/dates.txt") as f:
            count = sum(1 for line in f if datetime.strptime(line.strip(), "%Y-%m-%d").weekday() == 2)
        with open(f"{DATA_DIR}/dates-wednesdays.txt", "w") as f:
            f.write(str(count))
        return "/data/dates-wednesdays.txt"

    elif "sort contacts" in task:
        with open(f"{DATA_DIR}/contacts.json") as f:
            contacts = json.load(f)
        contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
        with open(f"{DATA_DIR}/contacts-sorted.json", "w") as f:
            json.dump(contacts, f, indent=2)
        return "/data/contacts-sorted.json"

    elif "most recent log files" in task:
        logs_dir = f"{DATA_DIR}/logs"
        logs = sorted(os.listdir(logs_dir), key=lambda x: os.path.getmtime(os.path.join(logs_dir, x)), reverse=True)[:10]
        with open(f"{DATA_DIR}/logs-recent.txt", "w") as f:
            for log in logs:
                with open(os.path.join(logs_dir, log)) as lf:
                    f.write(f"{log}:\n{lf.readline()}\n\n")  # Separate log entries properly
        return "/data/logs-recent.txt"

    elif "email sender" in task:
        with open(f"{DATA_DIR}/email.txt") as f:
            email_content = f.read()
        sender = query_llm(f"Extract sender's email from: {email_content}")
        with open(f"{DATA_DIR}/email-sender.txt", "w") as f:
            f.write(sender)
        return "/data/email-sender.txt"

    elif "credit card" in task:
        with open(f"{DATA_DIR}/credit-card.png", "rb") as f:
            image_data = f.read()
        try:
            card_number = query_llm("Extract card number from image", image_data)  # Ensure LLM supports image inputs
            if card_number:
                card_number = card_number.replace(" ", "")
            else:
                card_number = "Extraction failed"
        except Exception as e:
            card_number = f"Error: {str(e)}"

        with open(f"{DATA_DIR}/credit-card.txt", "w") as f:
            f.write(card_number)
        return "/data/credit-card.txt"

    elif "ticket sales" in task and "Gold" in task:
        conn = None
        try:
            conn = sqlite3.connect(f"{DATA_DIR}/ticket-sales.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
            total_sales = cursor.fetchone()[0] or 0
        except Exception as e:
            total_sales = f"Error: {str(e)}"
        finally:
            if conn:
                conn.close()

        with open(f"{DATA_DIR}/ticket-sales-gold.txt", "w") as f:
            f.write(str(total_sales))
        return "/data/ticket-sales-gold.txt"

    return None
