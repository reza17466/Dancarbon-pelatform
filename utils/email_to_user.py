"""Email notifications sent TO USERS (not the admin)."""
import smtplib
import ssl
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st


def _get_config():
    try:
        return {
            'sender': st.secrets.get("email", {}).get("sender", ""),
            'password': st.secrets.get("email", {}).get("password", ""),
        }
    except Exception:
        return {'sender': '', 'password': ''}


def _send(to_email, subject, html_body, text_body=None):
    cfg = _get_config()
    if not cfg['sender'] or not cfg['password']:
        return False
    if not to_email or '@' not in to_email:
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"DanCarbon Tech <{cfg['sender']}>"
        msg['To'] = to_email
        if text_body is None:
            text_body = re.sub(r'<[^>]+>', '', html_body)
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(cfg['sender'], cfg['password'])
            server.sendmail(cfg['sender'], to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def _base_template(title, color, body_html):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; color: #333;">
        <div style="text-align: center; padding: 20px; background: #1F3864; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">🌱 DanCarbon Tech</h1>
            <p style="color: #DEEAF6; margin: 5px 0 0 0;">CO₂ Separation Platform</p>
        </div>
        <div style="background: {color}; padding: 15px; text-align: center;">
            <h2 style="color: white; margin: 0;">{title}</h2>
        </div>
        <div style="background: #F8F9FA; padding: 25px; border-radius: 0 0 8px 8px;">
            {body_html}
            <hr style="border: none; border-top: 1px solid #DDD; margin: 25px 0;">
            <p style="font-size: 12px; color: #888; text-align: center;">
                This is an automated message from DanCarbon Tech Platform.<br>
                If you did not submit this contribution, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """


def send_accepted_email(to_email, title, description, score):
    subject = f"✅ Your contribution was accepted — DanCarbon Tech"
    body = f"""
    <p>Dear contributor,</p>
    <p><b>Thank you for your contribution to DanCarbon Tech!</b></p>
    <p>We are pleased to inform you that your submission has been
    <b style="color: #28A745;">accepted</b> by our AI filtering system
    and will be integrated into our shared CO₂ separation model.</p>
    <div style="background: white; padding: 15px; border-radius: 6px;
                border-left: 4px solid #28A745; margin: 20px 0;">
        <p style="margin: 0;"><b>Your submission:</b></p>
        <p style="margin: 10px 0 5px 0; font-size: 16px;">{title}</p>
        <p style="margin: 0; color: #666; font-size: 14px;">
            <b>AI Quality Score:</b> {score}/100
        </p>
    </div>
    <p><b>What happens next?</b></p>
    <ul>
        <li>Your contribution is now part of our shared knowledge base</li>
        <li>It may be used to improve our AI models</li>
        <li>You helped accelerate the green transition — thank you!</li>
    </ul>
    <p style="margin-top: 25px;">
        Your contribution matters. Together we are building a smarter,
        cleaner future for industrial gas separation.
    </p>
    <p>Best regards,<br>
    <b>Reza Chash</b><br>
    Founder & CEO, DanCarbon Tech</p>
    """
    return _send(to_email, subject, _base_template("Accepted", "#28A745", body))


def send_review_email(to_email, title, score):
    subject = f"⏳ Your contribution is under review — DanCarbon Tech"
    body = f"""
    <p>Dear contributor,</p>
    <p><b>Thank you for your contribution to DanCarbon Tech!</b></p>
    <p>Your submission has been received and is currently
    <b style="color: #FFA500;">under review</b> by our team.</p>
    <div style="background: white; padding: 15px; border-radius: 6px;
                border-left: 4px solid #FFA500; margin: 20px 0;">
        <p style="margin: 0;"><b>Your submission:</b></p>
        <p style="margin: 10px 0 5px 0; font-size: 16px;">{title}</p>
        <p style="margin: 0; color: #666; font-size: 14px;">
            <b>AI Quality Score:</b> {score}/100
        </p>
    </div>
    <p><b>What does this mean?</b></p>
    <ul>
        <li>Our AI gave your contribution a moderate score ({score}/100)</li>
        <li>A team member will review it manually</li>
        <li>We will notify you of the decision within 48 hours</li>
    </ul>
    <p><b>Can you improve your submission?</b></p>
    <p>To help us integrate your contribution faster, please consider including:</p>
    <ul>
        <li>Specific numbers (temperature, pressure, concentration)</li>
        <li>Units (K, bar, wt%, v/v)</li>
        <li>References (thesis, journal, DOI)</li>
    </ul>
    <p>Best regards,<br>
    <b>Reza Chash</b><br>
    Founder & CEO, DanCarbon Tech</p>
    """
    return _send(to_email, subject, _base_template("Under Review", "#FFA500", body))


def send_rejected_email(to_email, title, score, reason=None):
    subject = f"Update on your contribution — DanCarbon Tech"
    reason_text = reason or "Insufficient relevance or quality."
    body = f"""
    <p>Dear contributor,</p>
    <p>Thank you for taking the time to contribute to DanCarbon Tech.</p>
    <p>After review, we regret to inform you that your submission could not be
    integrated into our shared model at this time.</p>
    <div style="background: white; padding: 15px; border-radius: 6px;
                border-left: 4px solid #DC3545; margin: 20px 0;">
        <p style="margin: 0;"><b>Your submission:</b></p>
        <p style="margin: 10px 0 5px 0; font-size: 16px;">{title}</p>
        <p style="margin: 0; color: #666; font-size: 14px;">
            <b>AI Quality Score:</b> {score}/100<br>
            <b>Reason:</b> {reason_text}
        </p>
    </div>
    <p><b>Why was it rejected?</b></p>
    <p>Our AI filter evaluates contributions on relevance, quality, and
    consistency with existing data. Common reasons include:</p>
    <ul>
        <li>Missing specific numbers or data points</li>
        <li>Missing units (bar, K, wt%)</li>
        <li>No reference or source</li>
        <li>Content not directly related to CO₂ separation</li>
    </ul>
    <p><b>How to submit a better contribution?</b></p>
    <div style="background: #FFF4CE; padding: 15px; border-radius: 6px;
                border-left: 4px solid #FFC107;">
        <p style="margin: 0 0 10px 0;"><b>✅ Suggested structure:</b></p>
        <p style="margin: 0; font-size: 14px;">
        <b>Title:</b> CO₂ solubility in [solvent] at [temperature] and [pressure]<br><br>
        <b>Description:</b> Report the measured value with its unit.
        Include the reference (journal, thesis, or DOI).
        </p>
    </div>
    <p style="margin-top: 20px;">
    We would love to receive another contribution from you. If you have
    questions, feel free to reply to this email.
    </p>
    <p>Best regards,<br>
    <b>Reza Chash</b><br>
    Founder & CEO, DanCarbon Tech</p>
    """
    return _send(to_email, subject, _base_template("Not Accepted", "#DC3545", body))
