import requests
import time
import argparse
import threading
from cryptography.fernet import Fernet

# Generate encryption key (should be shared with the user securely)
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    return cipher.decrypt(encrypted_message.encode()).decode()

def fetch_and_encrypt_temp_mail(api_url, delete_url):
    """Fetch temporary emails, encrypt them, then delete from the server."""
    print("📩 Fetching temporary emails...")
    while True:
        response = requests.get(api_url)
        if response.status_code == 200:
            emails = response.json()
            for email in emails:
                encrypted_email = encrypt_message(email["message"])
                print(f"Encrypted Email: {encrypted_email}")
                
                # Delete from server after encryption
                requests.post(delete_url, json={"email_id": email["id"]})
                print("🗑️ Email Deleted from Server!")
        
        time.sleep(5)  # Fetch emails every 5 sec

def fetch_and_encrypt_sms(sms_api_url, delete_sms_url):
    """Fetch SMS, encrypt them, then delete from the server."""
    print("📩 Fetching SMS...")
    while True:
        response = requests.get(sms_api_url)
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                encrypted_sms = encrypt_message(msg["message"])
                print(f"Encrypted SMS: {encrypted_sms}")
                
                # Delete from server after encryption
                requests.post(delete_sms_url, json={"sms_id": msg["id"]})
                print("🗑️ SMS Deleted from Server!")
        
        time.sleep(5)  # Fetch every 5 seconds

def countdown_timer(duration, disable_url):
    """Countdown for 10 minutes and disable the number/email after time expires."""
    for remaining in range(duration, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r⏳ Self-Destructing in: {mins:02}:{secs:02}", end="", flush=True)
        time.sleep(1)
    
    print("\n💥 Time's up! Disabling temp resource...")
    requests.post(disable_url)
    print("🚫 Temporary Resource Destroyed!")

def main():
    parser = argparse.ArgumentParser(description="TempMail & TempSMS CLI with Encryption")
    parser.add_argument("--mode", choices=["email", "sms"], required=True, help="Choose 'email' for temp mail or 'sms' for temp number")
    args = parser.parse_args()
    
    if args.mode == "email":
        email_api = "https://example.com/api/get_temp_mail"
        delete_email_api = "https://example.com/api/delete_mail"
        disable_email_api = "https://example.com/api/revoke_mail"
        
        threading.Thread(target=fetch_and_encrypt_temp_mail, args=(email_api, delete_email_api)).start()
        countdown_timer(600, disable_email_api)  # 10 min countdown
    
    elif args.mode == "sms":
        sms_api = "https://example.com/api/get_temp_sms"
        delete_sms_api = "https://example.com/api/delete_sms"
        disable_sms_api = "https://example.com/api/revoke_sms"
        
        threading.Thread(target=fetch_and_encrypt_sms, args=(sms_api, delete_sms_api)).start()
        countdown_timer(600, disable_sms_api)  # 10 min countdown

if __name__ == "__main__":
    main()
