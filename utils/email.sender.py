"""
Email notification system using Gmail SMTP.
Sends an email to the admin whenever a form is submitted.
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st


# ==================================================
# CONFIGURATION
# ==================================================
# These are loaded from Streamlit secrets, with fallback for local dev.
# NEVER hardcode your app password in the code.

def _get_config():
    try:
        return {
            'sender': st.secrets.get("email", {}).get("sender", ""),
            'password': st.secrets.get("email", {}).get("password", ""),
            'recipient': st.secrets.get("email", {}).get("recipient", ""),
        }
    except Exception:
        # Local fallback — replace with your own for local testing
        return {
            'sender': '',
            'password': '',
            'recipient': '',
        }


def send_notification(subject, body_html):
    """Send an email notification to the admin."""
    cfg = _get_config()

    if not cfg['sender'] or not cfg['password'] or not cfg['recipient']:
        # Email not configured — log to file instead
        _log_to_file(subject, body_html)
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = cfg['sender']
        msg['To'] = cfg['recipient']

        # Plain text fallback
        text_part = MIMEText(_strip_html(body_html), 'plain')
        html_part = MIMEText(body_html, 'html')

        msg.attach(text_part)
        msg.attach(html_part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(cfg['sender'], cfg['password'])
            server.sendmail(cfg['sender'], cfg['recipient'], msg.as_string())

        return True
    except Exception as e:
        _log_to_file(f"ERROR sending: {subject}", str(e))
        return False


def _strip_html(html):
    import re
    return re.sub(r'<[^>]+>', '', html)


def _log_to_file(subject, body):
    """Fallback: save email content to local log file."""
    import os
    os.makedirs('data/logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = f'data/logs/email_{timestamp}.txt'
    with open(path, 'w') as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"Time: {datetime.now().isoformat()}\n")
        f.write(f"{'='*60}\n")
        f.write(body)


# ==================================================
# PUBLIC FUNCTIONS
# ==================================================

def notify_contribution(title, description, ctype, source, email, score, status):
    """Send email when someone submits a contribution."""
    subject = f"🌍 New Contribution: {title} (Score: {score})"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #1F3864;">🌍 New Contribution Submitted</h2>
        <table style="border-collapse: collapse;">
            <tr><td style="padding: 6px;"><b>Title:</b></td><td>{title}</td></tr>
            <tr><td style="padding: 6px;"><b>Type:</b></td><td>{ctype}</td></tr>
            <tr><td style="padding: 6px;"><b>Status:</b></td><td>{status}</td></tr>
            <tr><td style="padding: 6px;"><b>AI Score:</b></td><td>{score}/100</td></tr>
            <tr><td style="padding: 6px;"><b>Source:</b></td><td>{source or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Email:</b></td><td>{email or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Time:</b></td><td>{datetime.now().isoformat()}</td></tr>
        </table>
        <h3 style="color: #1F3864;">Description</h3>
        <p style="background: #F2F8FD; padding: 12px; border-radius: 6px;">{description}</p>
        <hr>
        <p style="color: #888; font-size: 12px;">DanCarbon Tech — Auto Notification</p>
    </body>
    </html>
    """
    return send_notification(subject, body)


def notify_quote_request(name, company, email, phone, country,
                          service, description, budget):
    """Send email when someone requests a quote."""
    subject = f"📩 New Quote Request from {name} ({company or 'N/A'})"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #1F3864;">📩 New Quote Request</h2>
        <table style="border-collapse: collapse;">
            <tr><td style="padding: 6px;"><b>Name:</b></td><td>{name}</td></tr>
            <tr><td style="padding: 6px;"><b>Company:</b></td><td>{company or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Email:</b></td><td>{email}</td></tr>
            <tr><td style="padding: 6px;"><b>Phone:</b></td><td>{phone or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Country:</b></td><td>{country or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Service:</b></td><td>{service}</td></tr>
            <tr><td style="padding: 6px;"><b>Budget:</b></td><td>{budget or '—'}</td></tr>
            <tr><td style="padding: 6px;"><b>Time:</b></td><td>{datetime.now().isoformat()}</td></tr>
        </table>
        <h3 style="color: #1F3864;">Description</h3>
        <p style="background: #F2F8FD; padding: 12px; border-radius: 6px;">{description}</p>
        <hr>
        <p style="color: #888; font-size: 12px;">DanCarbon Tech — Auto Notification</p>
    </body>
    </html>
    """
    return send_notification(subject, body)
