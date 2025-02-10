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

def handle_task(task_description):
    if "install uv" in task_description.lower():
        return run_uv_and_datagen()
    elif "format" in task_description.lower() and "prettier" in task_description.lower():
        return format_with_prettier()
    elif "count wednesdays" in task_description.lower():
        return count_wednesdays()
    elif "sort contacts" in task_description.lower():
        return sort_contacts()
    elif "most recent logs" in task_description.lower():
        return extract_recent_logs()
    elif "extract markdown titles" in task_description.lower():
        return extract_markdown_titles()
    elif "extract email sender" in task_description.lower():
        return extract_email_sender()
    elif "extract credit card number" in task_description.lower():
        return extract_credit_card_number()
    elif "find similar comments" in task_description.lower():
        return find_similar_comments()
    elif "calculate gold ticket sales" in task_description.lower():
        return calculate_gold_ticket_sales()
    else:
        raise ValueError("Unsupported task")

def run_uv_and_datagen():
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python", "-m", "urllib.request", "-o", "/tmp/datagen.py",
                    "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"], check=True)
    subprocess.run(["python", "/tmp/datagen.py", os.getenv("USER_EMAIL")], check=True)
    return "uv installed and datagen.py executed"

def format_with_prettier():
    subprocess.run(["npx", "prettier@3.4.2", "--write", f"{DATA_DIR}/format.md"], check=True)
    return "Formatted /data/format.md with prettier"

def count_wednesdays():
    with open(f"{DATA_DIR}/dates.txt", "r") as f:
        dates = f.readlines()
    count = sum(1 for date in dates if "Wed" in date)  # Adjust parsing as needed
    with open(f"{DATA_DIR}/dates-wednesdays.txt", "w") as f:
        f.write(str(count))
    return f"Counted {count} Wednesdays"

def sort_contacts():
    with open(f"{DATA_DIR}/contacts.json", "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open(f"{DATA_DIR}/contacts-sorted.json", "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "Sorted contacts"

def extract_recent_logs():
    log_files = sorted([f for f in os.listdir(f"{DATA_DIR}/logs") if f.endswith(".log")], reverse=True)[:10]
    lines = []
    for log in log_files:
        with open(f"{DATA_DIR}/logs/{log}", "r") as f:
            first_line = f.readline().strip()
            lines.append(first_line)
    with open(f"{DATA_DIR}/logs-recent.txt", "w") as f:
        f.write("\n".join(lines))
    return "Extracted recent log file lines"

def extract_markdown_titles():
    index = {}
    for filename in os.listdir(f"{DATA_DIR}/docs"):
        if filename.endswith(".md"):
            with open(f"{DATA_DIR}/docs/{filename}", "r") as f:
                for line in f:
                    if line.startswith("# "):
                        index[filename] = line[2:].strip()
                        break
    with open(f"{DATA_DIR}/docs/index.json", "w") as f:
        json.dump(index, f, indent=2)
    return "Extracted markdown titles"

def extract_email_sender():
    with open(f"{DATA_DIR}/email.txt", "r") as f:
        email_content = f.read()
    sender_email = query_llm(f"Extract the sender email from the following message:\n\n{email_content}")
    with open(f"{DATA_DIR}/email-sender.txt", "w") as f:
        f.write(sender_email)
    return "Extracted sender email"

def extract_credit_card_number():
    return "Not Implemented (Needs OCR)"

def find_similar_comments():
    return "Not Implemented (Needs embeddings)"

def calculate_gold_ticket_sales():
    return "Not Implemented (Needs SQL query)"
