# Blink10 - Temporary Email & SMS Session Tracker

## Summary

python script.py --email → Generate a new email.
python script.py --sms → Generate a new SMS number.
python script.py --list → View all past sessions.
python script.py --use <ID> → Switch back to a previous session.


## Overview

Blink10 is a simple terminal-based utility to generate and track temporary email addresses and SMS numbers. It allows users to:

- Generate disposable emails and SMS numbers
- Track previous sessions in an SQLite database
- Switch back to any previous session

## Features

- **Generate Temporary Emails**: Fetches disposable email domains and generates a random email.
- **Generate Temporary SMS Numbers**: Simulates SMS numbers for temporary use.
- **Session Tracking**: Saves sessions in an SQLite database to allow switching between them.
- **Session Management**: List and reuse previous sessions.

## Installation

### Requirements

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies (requirements.txt)

```
sqlite3
requests
argparse
```

## Usage

### Generate a new email session

```bash
python blink10.py --email
```

**Example Output:**

```
📧 New Email: user4821@tempmail.com
👉 Check manually: https://www.mailinator.com/v4/public/inboxes.jsp?to=user4821
```

### Generate a new SMS session

```bash
python blink10.py --sms
```

**Example Output:**

```
📱 New SMS Number: +1923847563
👉 Check manually: https://sms24.me/en/numbers/1923847563
```

### List all previous sessions

```bash
python blink10.py --list
```

**Example Output:**

```
📜 Previous Sessions:
1. Email: user4821@tempmail.com (Created: 2025-03-31 12:45:10)
2. SMS: +1923847563 (Created: 2025-03-31 12:46:05)
```

### Switch back to a previous session

```bash
python blink10.py --use <session_id>
```

**Example Output:**

```bash
python blink10.py --use 1
🔄 Switched to email session: user4821@tempmail.com
👉 Check manually: https://www.mailinator.com/v4/public/inboxes.jsp?to=user4821
```

## Notes

- Email and SMS services are not directly integrated. Users must check the respective links manually.
- Data is stored locally in an SQLite database (`sessions.db`).
- No sensitive data is stored, ensuring privacy.

##
