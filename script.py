import sqlite3
import argparse
import requests
import random

# Database setup
db = sqlite3.connect("sessions.db")
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
db.commit()

def generate_email():
    response = requests.get("https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/disposable_email_blocklist.conf")
    domains = response.text.splitlines()
    email = f"user{random.randint(1000,9999)}@{random.choice(domains)}"
    cursor.execute("INSERT INTO sessions (type, value) VALUES (?, ?)", ("email", email))
    db.commit()
    print(f"📧 New Email: {email}")
    print(f"👉 Check manually: https://www.mailinator.com/v4/public/inboxes.jsp?to={email.split('@')[0]}")

def generate_sms():
    response = requests.get("https://sms24.me/en")  # Simulated SMS number generation
    phone_number = f"+{random.randint(1000000000,9999999999)}"
    cursor.execute("INSERT INTO sessions (type, value) VALUES (?, ?)", ("sms", phone_number))
    db.commit()
    print(f"📱 New SMS Number: {phone_number}")
    print(f"👉 Check manually: https://sms24.me/en/numbers/{phone_number}")

def list_sessions():
    cursor.execute("SELECT id, type, value, created_at FROM sessions")
    rows = cursor.fetchall()
    if not rows:
        print("❌ No previous sessions found.")
        return
    print("📜 Previous Sessions:")
    for row in rows:
        print(f"{row[0]}. {row[1].capitalize()}: {row[2]} (Created: {row[3]})")

def use_session(session_id):
    cursor.execute("SELECT type, value FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    if not session:
        print("❌ Invalid session ID.")
        return
    session_type, value = session
    print(f"🔄 Switched to {session_type} session: {value}")
    if session_type == "email":
        print(f"👉 Check manually: https://www.mailinator.com/v4/public/inboxes.jsp?to={value.split('@')[0]}")
    elif session_type == "sms":
        print(f"👉 Check manually: https://sms24.me/en/numbers/{value}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", action="store_true", help="Generate a new email session")
    parser.add_argument("--sms", action="store_true", help="Generate a new SMS session")
    parser.add_argument("--list", action="store_true", help="List previous sessions")
    parser.add_argument("--use", type=int, help="Switch to a previous session by ID")
    args = parser.parse_args()
    
    if args.email:
        generate_email()
    elif args.sms:
        generate_sms()
    elif args.list:
        list_sessions()
    elif args.use:
        use_session(args.use)
    else:
        print("❌ No option selected. Use --help for available options.")

if __name__ == "__main__":
    main()
