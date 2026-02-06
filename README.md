# Domain Availability Monitor

Lightweight Python script to monitor domain availability and send alerts via **Email** and **Telegram**.

---

## Setup

Create `.env`:

```
GMAIL_EMAIL=your_email
GMAIL_APP_PASSWORD=your_app_password
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

Edit:

* `domains.json` → domains to monitor
* `config.py` → intervals, cooldown, recipients

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python monitor.py
```

---

## Run in Background

### Linux

**Option 1 – nohup**

```bash
nohup python monitor.py > monitor.log 2>&1 &
```

Stop:

```bash
ps aux | grep monitor.py
kill <pid>
```

**Option 2 – screen (recommended)**

```bash
screen -S domain-monitor
python monitor.py
```

Detach:

```
CTRL+A, D
```

Reattach:

```bash
screen -r domain-monitor
```

---

### Windows

**Option 1 – PowerShell background job**

```powershell
Start-Process python -ArgumentList "monitor.py"
```

**Option 2 – Run minimized**

```powershell
pythonw monitor.py
```

---

## Notes

* Use Gmail **App Password**
* DNS availability ≠ guaranteed registration availability

---