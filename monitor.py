# script.py

import dns.resolver
import time
import datetime
import json
import smtplib
import requests
from email.message import EmailMessage

# ✅ Import everything from config.py
from config import (
    SMTP_EMAIL,
    SMTP_APP_PASSWORD,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_IDS,
    ALERT_TO_EMAILS,
    CHECK_INTERVAL,
    DNS_TIMEOUT,
    ALERT_COOLDOWN,
    DOMAINS_FILE,
)

# Track last alert time per domain
last_alert_sent = {}


def load_domains():
    with open(DOMAINS_FILE, "r") as f:
        data = json.load(f)
    return data.get("domains", [])


def is_domain_available(domain):
    resolver = dns.resolver.Resolver()
    resolver.lifetime = DNS_TIMEOUT

    try:
        resolver.resolve(domain, "NS")
        return False
    except dns.resolver.NXDOMAIN:
        return True
    except dns.resolver.NoAnswer:
        return True
    except Exception:
        return False


def confirm_available(domain):
    """Double confirmation to avoid DNS glitches"""
    return is_domain_available(domain) and is_domain_available(domain)


def send_email(smtp, domain):
    for email in ALERT_TO_EMAILS:
        msg = EmailMessage()
        msg["Subject"] = f"🚀 DOMAIN AVAILABLE: {domain}"
        msg["From"] = SMTP_EMAIL
        msg["To"] = email

        msg.set_content(
            f"""
Domain Available Alert 🚀

The domain "{domain}" appears to be AVAILABLE.

Time: {datetime.datetime.now()}
"""
        )
        smtp.send_message(msg)


def send_telegram(domain):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_IDS:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for chat_id in TELEGRAM_CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": f"🚀 DOMAIN AVAILABLE\n\n{domain}\n\nTime: {datetime.datetime.now()}"
        }

        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"⚠️ Telegram error for {chat_id}: {e}")


def main():
    print("📡 Domain availability monitor started")
    print("Press CTRL+C to stop\n")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_APP_PASSWORD)

            while True:
                domains = load_domains()
                now = datetime.datetime.now()
                now_ts = time.time()

                for domain in domains:
                    available = confirm_available(domain)
                    print(f"[{now}] {domain} → available: {available}")

                    if available:
                        last_time = last_alert_sent.get(domain, 0)

                        if now_ts - last_time >= ALERT_COOLDOWN:
                            send_email(smtp, domain)
                            send_telegram(domain)
                            last_alert_sent[domain] = now_ts
                            print(f"📧📲 Alert sent for {domain}")

                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user")


if __name__ == "__main__":
    main()
