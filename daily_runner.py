"""daily_runner.py - اجرای روزانه کامل اسکنر."""
import json
import logging
import os
import sys
import traceback
from datetime import datetime

from core.scanner import Scanner
from core.report import ReportGenerator
from core.telegram_notifier import TelegramNotifier, detect_psiphon_proxy

os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", handlers=[logging.FileHandler(f"logs/daily_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding="utf-8"), logging.StreamHandler(sys.stdout)])
log = logging.getLogger("daily_runner")


def load_telegram_config():
    path = "config/telegram.json"
    config = {"enabled": True, "send_top_n": 20, "attach_csv": True, "proxy": "auto"}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        config["bot_token"] = os.environ["TELEGRAM_BOT_TOKEN"]
    if os.environ.get("TELEGRAM_CHAT_ID"):
        config["chat_id"] = os.environ["TELEGRAM_CHAT_ID"]
    if os.environ.get("TELEGRAM_PROXY") is not None:
        config["proxy"] = os.environ["TELEGRAM_PROXY"]
    if not config.get("enabled", False):
        return None
    token, chat_id = config.get("bot_token", ""), config.get("chat_id", "")
    if not token or "PUT_YOUR" in token or not chat_id or "PUT_YOUR" in str(chat_id):
        log.warning("توکن یا chat_id تلگرام تنظیم نشده.")
        return None
    return config


def _telegram_proxy(config):
    proxy = config.get("proxy")
    if proxy == "direct":
        return None
    if proxy and proxy != "auto":
        return proxy
    return detect_psiphon_proxy()


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
                notifier = TelegramNotifier(token=telegram_config["bot_token"], chat_id=telegram_config["chat_id"], proxy=_telegram_proxy(telegram_config))
                sent = notifier.send_results(results, limit=telegram_config.get("send_top_n", 20))
                log.info("پیام نتایج با موفقیت ارسال شد." if sent else "ارسال پیام به تلگرام ناموفق بود.")
                if telegram_config.get("attach_csv", True) and os.path.exists("reports/scan_result.csv"):
                    notifier.send_file("reports/scan_result.csv", caption=f"گزارش کامل اسکن - {datetime.now().strftime('%Y-%m-%d')}")
            except Exception:
                log.error("خطا در ارسال تلگرام:\n%s", traceback.format_exc())
        log.info("اجرای روزانه با موفقیت تمام شد.")
        return 0
    except Exception:
        error_text = traceback.format_exc()
        log.error("خطای کلی در اجرای روزانه:\n%s", error_text)
        try:
            telegram_config = load_telegram_config()
            if telegram_config:
                notifier = TelegramNotifier(token=telegram_config["bot_token"], chat_id=telegram_config["chat_id"], proxy=_telegram_proxy(telegram_config))
                notifier.send_message(f"⚠️ خطا در اجرای روزانه اسکنر:\n{error_text[-3500:]}", parse_mode=None)
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(run())
