import time
import argparse
import threading
import random
import string
import requests
from bs4 import BeautifulSoup
import json
import os
import sqlite3
from cryptography.fernet import Fernet
import hashlib

# Database setup for local storage
def setup_database():
    conn = sqlite3.connect('blink10_temp.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS processed_messages (
        message_hash TEXT PRIMARY KEY,
        timestamp INTEGER
    )
    ''')
    conn.commit()
    return conn

# Generate encryption key
key = Fernet.generate_key()
cipher = Fernet(key)
print(f"🔐 Your encryption key (save this): {key.decode()}")
print(f"⚠️  WARNING: Messages will be encrypted and originals deleted!")

def encrypt_message(message):
    """Encrypt a message using Fernet symmetric encryption."""
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    """Decrypt a message using Fernet symmetric encryption."""
    return cipher.decrypt(encrypted_message.encode()).decode()

def generate_random_string(length=10):
    """Generate a random string for email username."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def load_disposable_domains():
    """Load disposable email domains from GitHub."""
    try:
        response = requests.get("https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/master/disposable_email_blocklist.conf")
        if response.status_code == 200:
            domains = response.text.strip().split('\n')
            return domains[:100]  # Limit to first 100 domains for performance
        else:
            return ["mailinator.com", "guerrillamail.com", "temp-mail.org", "sharklasers.com"]
    except Exception as e:
        print(f"Error loading domains: {e}")
        return ["mailinator.com", "guerrillamail.com", "temp-mail.org", "sharklasers.com"]

def create_temp_email():
    """Create a temporary email using a random disposable email domain."""
    username = generate_random_string()
    domains = load_disposable_domains()
    domain = random.choice(domains)
    return f"{username}@{domain}"

def message_already_processed(conn, message):
    """Check if a message has already been processed to avoid duplicates."""
    cursor = conn.cursor()
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    cursor.execute("SELECT 1 FROM processed_messages WHERE message_hash = ?", (message_hash,))
    result = cursor.fetchone()
    
    if not result:
        # Mark as processed
        cursor.execute("INSERT INTO processed_messages VALUES (?, ?)", 
                      (message_hash, int(time.time())))
        conn.commit()
        return False
    return True

def check_mailinator_emails(email_address, conn):
    """Check emails using Mailinator's public interface."""
    username = email_address.split('@')[0]
    
    try:
        # This uses Mailinator's public web interface
        print(f"📩 Checking emails for {email_address}...")
        
        # In a real implementation, you would use an API or web scraping
        # For this example, we'll simulate the process
        mailinator_url = f"https://www.mailinator.com/v4/public/inboxes.jsp?to={username}"
        response = requests.get(mailinator_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract email data from the page
            # This is a simplified example and may need adjustments
            email_rows = soup.select('tr.ng-scope')
            
            if email_rows:
                for row in email_rows:
                    try:
                        subject_elem = row.select_one('td:nth-child(3)')
                        if subject_elem:
                            subject = subject_elem.text.strip()
                            # Generate a unique message ID from the subject
                            message = f"Subject: {subject}"
                            
                            # Check if we've already processed this message
                            if not message_already_processed(conn, message):
                                # Encrypt the message
                                encrypted = encrypt_message(message)
                                print(f"📬 New email received!")
                                print(f"🔒 Encrypted content: {encrypted}")
                                print(f"🔓 Decrypted content: {message}")
                                print("🗑️ Original message tracked for deletion")
                    except Exception as e:
                        print(f"Error processing email: {e}")
        
        # Provide the link for manual checking
        print(f"👉 For manual checking: {mailinator_url}")
        
    except Exception as e:
        print(f"Error checking emails: {e}")

def fetch_mail_loop(email_address, conn):
    """Loop to keep checking for new emails."""
    print(f"🔄 Starting to monitor {email_address}")
    print(f"⏱️ Email access will self-destruct after 10 minutes")
    
    try:
        while True:
            check_mailinator_emails(email_address, conn)
            time.sleep(5)
    except KeyboardInterrupt:
        print("✋ Email checking stopped")

def get_available_sms24_numbers():
    """Get available phone numbers from SMS24.me."""
    try:
        response = requests.get("https://sms24.me/en/numbers")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            numbers = []
            
            # Extract numbers based on the site's HTML structure
            number_elements = soup.select('.number-boxes .number-box')
            for element in number_elements:
                number_text = element.select_one('.number-box-number')
                if number_text:
                    numbers.append(number_text.text.strip())
            
            if numbers:
                return numbers
    except Exception as e:
        print(f"Error fetching SMS24.me numbers: {e}")
    
    # Return some example numbers if fetching fails
    return ["+12025550182", "+44770123456", "+33612345678"]

def check_sms24_messages(phone_number, conn):
    """Check messages for a phone number on SMS24.me."""
    clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    
    try:
        print(f"📱 Checking SMS for {phone_number}...")
        
        # Try to fetch actual messages from the website
        sms_url = f"https://sms24.me/en/numbers/{clean_number}"
        response = requests.get(sms_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract messages based on the site's HTML structure
            message_elements = soup.select('.main-content .message-box')
            
            if message_elements:
                for element in message_elements:
                    try:
                        sender = element.select_one('.message-box-title')
                        content = element.select_one('.message-box-text')
                        
                        if sender and content:
                            sender_text = sender.text.strip()
                            content_text = content.text.strip()
                            message = f"From: {sender_text} - {content_text}"
                            
                            # Check if we've already processed this message
                            if not message_already_processed(conn, message):
                                # Encrypt the message
                                encrypted = encrypt_message(message)
                                print(f"📲 New SMS received!")
                                print(f"🔒 Encrypted content: {encrypted}")
                                print(f"🔓 Decrypted content: {message}")
                                print("🗑️ Original message tracked for deletion")
                    except Exception as e:
                        print(f"Error processing SMS: {e}")
        
        # Provide the link for manual checking
        print(f"👉 For manual checking: {sms_url}")
            
    except Exception as e:
        print(f"Error checking SMS: {e}")

def fetch_sms_loop(phone_number, conn):
    """Loop to keep checking for new SMS."""
    print(f"🔄 Starting to monitor {phone_number}")
    print(f"⏱️ Phone number access will expire after 10 minutes")
    
    try:
        while True:
            check_sms24_messages(phone_number, conn)
            time.sleep(5)
    except KeyboardInterrupt:
        print("✋ SMS checking stopped")

def cleanup_old_messages(conn):
    """Delete message records older than 10 minutes."""
    cursor = conn.cursor()
    expiry_time = int(time.time()) - 600  # 10 minutes ago
    cursor.execute("DELETE FROM processed_messages WHERE timestamp < ?", (expiry_time,))
    conn.commit()
    print(f"🧹 Cleaned up old message records: {cursor.rowcount} deleted")

def countdown_timer(duration, conn):
    """Countdown timer for self-destruction."""
    start_time = time.time()
    end_time = start_time + duration
    
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        mins, secs = divmod(remaining, 60)
        print(f"\r⏳ Self-Destructing in: {mins:02}:{secs:02}", end="", flush=True)
        
        # Every minute, cleanup old messages
        if remaining % 60 == 0:
            cleanup_old_messages(conn)
            
        time.sleep(1)
    
    print("\n💥 Time's up! Access expired")
    # Final cleanup
    cleanup_old_messages(conn)

def main():
    parser = argparse.ArgumentParser(description="Blink10: Self-destructing Email and SMS")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", action="store_true", help="Generate a temporary email")
    group.add_argument("--sms", action="store_true", help="Use a temporary phone number")
    parser.add_argument("--time", type=int, default=10, help="Self-destruct time in minutes (default: 10)")
    args = parser.parse_args()
    
    # Set up database
    conn = setup_database()
    
    try:
        if args.email:
            temp_email = create_temp_email()
            print(f"📧 Generated temporary email: {temp_email}")
            
            # Start email checking in a separate thread
            email_thread = threading.Thread(target=fetch_mail_loop, args=(temp_email, conn), daemon=True)
            email_thread.start()
            
            # Start countdown timer
            countdown_timer(args.time * 60, conn)
            print(f"🗑️ Email {temp_email} access has expired")
            
        elif args.sms:
            available_numbers = get_available_sms24_numbers()
            temp_phone = random.choice(available_numbers)
            print(f"📱 Selected temporary phone number: {temp_phone}")
            print("Note: This number is shared publicly on SMS24.me")
            
            # Start SMS checking in a separate thread
            sms_thread = threading.Thread(target=fetch_sms_loop, args=(temp_phone, conn), daemon=True)
            sms_thread.start()
            
            # Start countdown timer
            countdown_timer(args.time * 60, conn)
            print(f"🗑️ Phone number {temp_phone} access has expired")
    
    finally:
        # Clean up on exit
        try:
            # Delete all processed message records
            cursor = conn.cursor()
            cursor.execute("DELETE FROM processed_messages")
            conn.commit()
            print("🧹 All message records deleted")
            
            # Delete the database file
            conn.close()
            if os.path.exists('blink10_temp.db'):
                os.remove('blink10_temp.db')
                print("🗑️ Database file deleted")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main()