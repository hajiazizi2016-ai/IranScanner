"""
daily_runner.py
----------------
اجرای روزانه‌ی کامل اسکنر:
  ۱. اسکن بازار و پیدا کردن سیگنال‌ها
  ۲. ذخیره گزارش CSV
  ۳. ارسال نتایج به تلگرام (در صورت فعال بودن در config/telegram.json)

نحوه اجرای دستی:
    python daily_runner.py

نحوه اجرای خودکار روزانه (پیشنهادی):
  ویندوز -> Task Scheduler:
    برنامه: مسیر python.exe شما (مثلا C:\\Users\\you\\project\\.venv\\Scripts\\python.exe)
    آرگومان: مسیر کامل این فایل (daily_runner.py)
    شروع در: مسیر پوشه پروژه
    Trigger: هر روز ساعت مشخص (مثلا بعد از بسته شدن بازار)

  لینوکس/مک -> cron:
    0 16 * * 6,0,1,2,3   cd /path/to/IranScanner && /path/to/venv/bin/python daily_runner.py
    (بورس ایران شنبه تا چهارشنبه فعاله - روزهای هفته را طبق نیاز تنظیم کنید)
"""

import json
import logging
import os
import sys
import traceback
from datetime import datetime

from core.scanner import Scanner
from core.report import ReportGenerator
from core.telegram_notifier import TelegramNotifier, detect_psiphon_proxy


# ==========================================
# لاگ‌گیری
# ==========================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            f"logs/daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

log = logging.getLogger("daily_runner")


# ==========================================
# خواندن تنظیمات تلگرام
# ==========================================

def load_telegram_config():

    path = "config/telegram.json"

    config = {
        "enabled": True,
        "send_top_n": 20,
        "attach_csv": True,
        "proxy": "auto"
    }

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))

    # اولویت با متغیرهای محیطی (GitHub Actions Secrets) است تا
    # توکن واقعی هیچ‌وقت لازم نباشد داخل ریپازیتوری کامیت شود.
    env_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    env_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    env_proxy = os.environ.get("TELEGRAM_PROXY")

    if env_token:
        config["bot_token"] = env_token

    if env_chat_id:
        config["chat_id"] = env_chat_id

    if env_proxy is not None:
        config["proxy"] = env_proxy

    if not config.get("enabled", False):
        log.info("ارسال تلگرام در تنظیمات غیرفعال است (enabled=false).")
        return None

    token = config.get("bot_token", "")
    chat_id = config.get("chat_id", "")

    if not token or "PUT_YOUR" in token or not chat_id or "PUT_YOUR" in str(chat_id):
        log.warning(
            "توکن یا chat_id تلگرام تنظیم نشده "
            "(نه در config/telegram.json و نه در متغیرهای محیطی)."
        )
        return None

    return config


# ==========================================
# اجرای اصلی
# ==========================================

def run():

    log.info("=" * 60)
    log.info("شروع اجرای روزانه اسکنر - %s", datetime.now().isoformat())
    log.info("=" * 60)

    try:
        scanner = Scanner()
        results = scanner.scan()

        log.info("تعداد سیگنال‌های پیدا‌شده: %d", len(results))

        scanner.print_result(results)

        reporter = ReportGenerator()
        reporter.export_scan(results)

        telegram_config = load_telegram_config()

        if telegram_config:

            try:

                notifier = TelegramNotifier(
                    token=telegram_config["bot_token"],
                    chat_id=telegram_config["chat_id"],
                    proxy=(
                        None
                        if telegram_config.get("proxy") == "direct"
                        else (
                            telegram_config.get("proxy")
                            if telegram_config.get("proxy") and telegram_config.get("proxy") != "auto"
                            else detect_psiphon_proxy()
                        )
                    )
                )

                sent = notifier.send_results(
                    results,
                    limit=telegram_config.get("send_top_n", 20)
                )

                if sent:
                    log.info("پیام نتایج با موفقیت به تلگرام ارسال شد.")
                else:
                    log.error("ارسال پیام به تلگرام ناموفق بود.")

                if telegram_config.get("attach_csv", True):

                    csv_path = "reports/scan_result.csv"

                    if os.path.exists(csv_path):
                        notifier.send_file(
                            csv_path,
                            caption=f"گزارش کامل اسکن - {datetime.now().strftime('%Y-%m-%d')}"
                        )

            except Exception:
                log.error("خطا در ارسال تلگرام:\n%s", traceback.format_exc())

        log.info("اجرای روزانه با موفقیت تمام شد.")
        return 0

    except Exception:

        log.error("خطای کلی در اجرای روزانه:\n%s", traceback.format_exc())

        # اگر تلگرام تنظیم شده باشد، خطا را هم به تلگرام اطلاع بده
        try:
            telegram_config = load_telegram_config()
            if telegram_config:
                notifier = TelegramNotifier(
                    token=telegram_config["bot_token"],
                    chat_id=telegram_config["chat_id"],
                    proxy=(
                        None
                        if telegram_config.get("proxy") == "direct"
                        else (
                            telegram_config.get("proxy")
                            if telegram_config.get("proxy") and telegram_config.get("proxy") != "auto"
                            else detect_psiphon_proxy()
                        )
                    )
                )
                notifier.send_message(
                    f"⚠️ خطا در اجرای روزانه اسکنر:\n<code>{traceback.format_exc()[-800:]}</code>"
                )
        except Exception:
            pass

        return 1


if __name__ == "__main__":
    sys.exit(run())
