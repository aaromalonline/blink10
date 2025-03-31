# Blink10

**Blink10** is a command-line tool for creating **self-destructing temporary emails and phone numbers** that expire after **10 minutes**. It ensures user privacy by **deleting received messages after fetching** and applying encryption before deletion.

---
## Features
- **Temporary Emails** 📧: Generate a disposable email address valid for **10 minutes**.
- **Temporary Phone Numbers** 📱: Get a self-destructing phone number (if supported by provider).
- **Auto-Fetch Messages** ⏳: Continuously fetch received emails or SMS until expiry.
- **End-to-End Encryption** 🔐: Encrypts messages before deletion for added privacy.
- **Fully Automated Expiry** 💥: Automatically deletes emails, SMS, and generated IDs after **10 minutes**.

---
## Installation
```sh
# Clone the repository
git clone https://github.com/yourusername/blink10.git
cd blink10

# Install dependencies
pip install -r requirements.txt
```

---
## Usage

### 1️⃣ Generate a Temporary Email
```sh
python blink10.py --email
```
- Displays the **generated email address**.
- Fetches received emails every few seconds.
- Deletes messages **after they are fetched**.
- Auto-expires in **10 minutes**.

### 2️⃣ Generate a Temporary Phone Number
```sh
python blink10.py --sms
```
- Displays the **generated temporary phone number**.
- Fetches incoming SMS until expiry.
- Auto-deletes messages and number after **10 minutes**.

### 3️⃣ Encrypt Received Messages Before Deletion
```sh
python blink10.py --email --encrypt
```
- Uses encryption to **scramble messages** before deletion.
- Only decryptable using a **local private key**.

### 4️⃣ Custom Timer for Expiry
```sh
python blink10.py --email --time 5
```
- Changes the expiration time to **5 minutes** (default is 10 min).

---
## Security & Privacy
**How Blink10 Protects Your Privacy:**
- **Messages auto-delete after fetching.**
- **Temporary IDs (email/number) are completely removed** after expiry.
- **Encryption ensures the server never stores readable messages.**

---
## Example Output
```sh
$ python blink10.py --email
[+] Temporary Email: xyz123@blinkmail.com
[+] Fetching emails...
[+] New Email Received: "Verification Code: 875421"
[+] Email deleted after fetching.
[+] Self-destructing in: 9m 30s...
```

```sh
$ python blink10.py --sms
[+] Temporary Phone Number: +1234567890
[+] Fetching SMS...
[+] New SMS Received: "Your OTP is 567890"
[+] SMS deleted after fetching.
[+] Self-destructing in: 8m 45s...
```

---
## License
Blink10 is an **open-source** project. Feel free to contribute and improve privacy-focused communication! 🚀

