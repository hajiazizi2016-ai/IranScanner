import logging

import os

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailNotifier:
    """
    ارسال نتایج اسکنر با ایمیل (پیش‌فرض: Gmail SMTP).

    نحوه ساخت:
      ۱. یک جیمیل بساز (یا از جیمیل فعلیت استفاده کن)
      ۲. برو به: https://myaccount.google.com/apppasswords
      ۳. یک "App Password" ۱۶ کاراکتری بساز (نیاز به فعال بودن
         تایید دو مرحله‌ای دارد - اگر نداری، اول از تنظیمات
         امنیتی جیمیل فعالش کن)
      ۴. آن ۱۶ کاراکتر را (نه پسورد اصلی جیمیلت را) در تنظیمات
         این برنامه استفاده کن

    نکته: ایمیل در ایران فیلتر نیست، پس این بخش نیازی به VPN ندارد.
    """

    def __init__(
        self,
        sender_email,
        app_password,
        recipient_email,
        smtp_host="smtp.gmail.com",
        smtp_port=587
    ):

        if not sender_email or not app_password or not recipient_email:
            raise ValueError(
                "تنظیمات ایمیل کامل نیست. فایل config/email.json را پر کنید."
            )

        self.sender_email = sender_email
        self.app_password = app_password
        self.recipient_email = recipient_email
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, subject, html_body, attachment_path=None):

        try:

            msg = MIMEMultipart()

            msg["From"] = self.sender_email
            msg["To"] = self.recipient_email
            msg["Subject"] = subject

            msg.attach(MIMEText(html_body, "html", "utf-8"))

            if attachment_path and os.path.exists(attachment_path):

                with open(attachment_path, "rb") as f:

                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())

                encoders.encode_base64(part)

                filename = os.path.basename(attachment_path)

                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}"
                )

                msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:

                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            return True

        except Exception as e:

            logging.error("EMAIL SEND FAILED: %s", e, exc_info=True)

            return False

    def format_results_html(self, results, limit=50):

        if not results:
            return "<p>امروز هیچ سیگنالی پیدا نشد.</p>"

        rows_html = ""

        for s in results[:limit]:

            symbol = getattr(s, "symbol", "")
            score = round(getattr(s, "final_score", getattr(s, "final_rank", 0)), 1)
            rr = round(getattr(s, "rr", 0), 2)
            rr_power = round(getattr(s, "rr_power", 0), 2)
            vol_ratio = round(getattr(s, "volume_ratio", 0), 2)
            buyer_power = round(getattr(s, "buyer_power", 0), 2)
            reason = getattr(s, "smart_money_reason", "") or getattr(s, "validation_reason", "")

            rows_html += f"""
            <tr>
                <td style="padding:6px; border:1px solid #ddd;">{symbol}</td>
                <td style="padding:6px; border:1px solid #ddd;">{score}</td>
                <td style="padding:6px; border:1px solid #ddd;">{rr}</td>
                <td style="padding:6px; border:1px solid #ddd;">{rr_power}</td>
                <td style="padding:6px; border:1px solid #ddd;">{vol_ratio}x</td>
                <td style="padding:6px; border:1px solid #ddd;">{buyer_power}</td>
                <td style="padding:6px; border:1px solid #ddd; direction:rtl;">{reason}</td>
            </tr>
            """

        html = f"""
        <html dir="rtl">
        <body style="font-family: Tahoma, sans-serif;">
            <h2>نتایج اسکن امروز — {len(results)} سیگنال</h2>
            <table style="border-collapse: collapse; width:100%;">
                <tr style="background:#f0f0f0;">
                    <th style="padding:6px; border:1px solid #ddd;">نماد</th>
                    <th style="padding:6px; border:1px solid #ddd;">امتیاز</th>
                    <th style="padding:6px; border:1px solid #ddd;">RR</th>
                    <th style="padding:6px; border:1px solid #ddd;">قدرت RR</th>
                    <th style="padding:6px; border:1px solid #ddd;">حجم</th>
                    <th style="padding:6px; border:1px solid #ddd;">قدرت خریدار</th>
                    <th style="padding:6px; border:1px solid #ddd;">دلیل</th>
                </tr>
                {rows_html}
            </table>
            <p>فایل CSV کامل پیوست است.</p>
        </body>
        </html>
        """

        return html
