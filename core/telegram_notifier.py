import logging

import subprocess

import requests


def detect_psiphon_proxy(timeout=5):
    """
    پورت پراکسی سایفون هر بار که برنامه دوباره باز می‌شه عوض می‌شود.
    این تابع به‌صورت خودکار (فقط روی ویندوز) پورت‌های باز شده توسط
    psiphon-tunnel-core.exe را پیدا می‌کند و اولین پورتی که واقعاً
    به عنوان SOCKS5 به تلگرام وصل می‌شود را برمی‌گرداند.
    """

    try:

        netstat = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            timeout=10
        ).stdout

        tasklist = subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
            timeout=10
        ).stdout

        psiphon_pids = set()

        for line in tasklist.splitlines():
            if "psiphon" in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    psiphon_pids.add(parts[1])

        if not psiphon_pids:
            logging.warning("پروسه psiphon-tunnel-core.exe پیدا نشد.")
            return None

        candidate_ports = []

        for line in netstat.splitlines():

            if "127.0.0.1:" not in line or "LISTENING" not in line:
                continue

            parts = line.split()

            if len(parts) < 5:
                continue

            pid = parts[-1]

            if pid not in psiphon_pids:
                continue

            addr = parts[1]

            try:
                port = int(addr.rsplit(":", 1)[1])
                candidate_ports.append(port)
            except (ValueError, IndexError):
                continue

        for port in candidate_ports:

            try:

                r = requests.get(
                    "https://api.telegram.org",
                    proxies={"https": f"socks5h://127.0.0.1:{port}"},
                    timeout=timeout
                )

                if r.status_code == 200:
                    logging.info("پراکسی سایفون به‌صورت خودکار پیدا شد: %s", port)
                    return f"socks5h://127.0.0.1:{port}"

            except Exception:
                continue

        logging.warning("هیچ‌کدام از پورت‌های سایفون به تلگرام وصل نشدند.")

        return None

    except Exception as e:

        logging.warning("خطا در تشخیص خودکار پراکسی سایفون: %s", e)

        return None


class TelegramNotifier:
    """
    ارسال نتایج اسکنر به یک ربات تلگرام.

    نحوه ساخت ربات:
      ۱. در تلگرام به @BotFather پیام بده و با دستور /newbot یک ربات بساز
         تا یک TOKEN شبیه این بگیری: 123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      ۲. برای گرفتن chat_id: به رباتت یک پیام بده، بعد این آدرس رو در مرورگر باز کن:
         https://api.telegram.org/bot<TOKEN>/getUpdates
         و مقدار "chat":{"id": ...} رو بردار.
         (اگر می‌خوای به یک گروه/کانال بفرستی، ربات رو به اون گروه/کانال اضافه کن
         و chat_id گروه/کانال رو همون‌جا پیدا کن)
    """

    API_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token, chat_id, proxy=None):

        if not token or not chat_id:
            raise ValueError(
                "Telegram token/chat_id تنظیم نشده. فایل config/telegram.json را پر کنید."
            )

        self.token = token
        self.chat_id = chat_id

        # اگر api.telegram.org مستقیم در دسترس نباشد (فیلترینگ)،
        # می‌توان از یک پراکسی محلی VPN استفاده کرد.
        # مثال در config/telegram.json:
        #   "proxy": "socks5h://127.0.0.1:1080"
        #   "proxy": "http://127.0.0.1:8080"
        self.proxies = None

        if proxy:
            self.proxies = {
                "http": proxy,
                "https": proxy
            }

    # ==========================================
    # ارسال یک پیام متنی ساده (با شکستن خودکار پیام‌های طولانی)
    # ==========================================

    def send_message(self, text, parse_mode="HTML"):

        url = self.API_URL.format(
            token=self.token,
            method="sendMessage"
        )

        # تلگرام حداکثر 4096 کاراکتر در هر پیام قبول می‌کند
        max_len = 4000

        chunks = [
            text[i:i + max_len]
            for i in range(0, len(text), max_len)
        ] or [""]

        ok = True

        for chunk in chunks:

            try:

                resp = requests.post(
                    url,
                    data={
                        "chat_id": self.chat_id,
                        "text": chunk,
                        "parse_mode": parse_mode,
                        "disable_web_page_preview": True
                    },
                    proxies=self.proxies,
                    timeout=15
                )

                if resp.status_code != 200:
                    logging.error("TELEGRAM ERROR: %s %s", resp.status_code, resp.text)
                    ok = False

            except Exception as e:

                logging.error("TELEGRAM SEND FAILED: %s", e, exc_info=True)
                ok = False

        return ok

    # ==========================================
    # ارسال یک فایل (مثلا CSV گزارش روزانه)
    # ==========================================

    def send_file(self, file_path, caption=""):

        url = self.API_URL.format(
            token=self.token,
            method="sendDocument"
        )

        try:

            with open(file_path, "rb") as f:

                resp = requests.post(
                    url,
                    data={
                        "chat_id": self.chat_id,
                        "caption": caption
                    },
                    files={"document": f},
                    proxies=self.proxies,
                    timeout=30
                )

            if resp.status_code != 200:
                logging.error("TELEGRAM FILE ERROR: %s %s", resp.status_code, resp.text)
                return False

            return True

        except Exception as e:

            logging.error("TELEGRAM FILE SEND FAILED: %s", e, exc_info=True)
            return False

    # ==========================================
    # فرمت‌بندی و ارسال نتایج اسکنر به‌صورت پیام خوانا
    # ==========================================

    def format_results(self, results, limit=20):

        if not results:
            return "امروز هیچ سیگنالی پیدا نشد. 🔍"

        lines = []

        lines.append(f"📊 <b>نتایج اسکن امروز</b> — {len(results)} سیگنال\n")

        for s in results[:limit]:

            symbol = getattr(s, "symbol", "")
            score = round(getattr(s, "final_score", getattr(s, "final_rank", 0)), 1)
            rr = round(getattr(s, "rr", 0), 2)
            rr_power = round(getattr(s, "rr_power", 0), 2)
            vol_ratio = round(getattr(s, "volume_ratio", 0), 2)
            buyer_power = round(getattr(s, "buyer_power", 0), 2)
            reason = getattr(s, "smart_money_reason", "") or getattr(s, "validation_reason", "")

            lines.append(
                f"🔹 <b>{symbol}</b> | امتیاز: {score}\n"
                f"   RR: {rr} | قدرت RR: {rr_power} | حجم: {vol_ratio}x | قدرت خریدار: {buyer_power}\n"
                f"   {reason}"
            )

        if len(results) > limit:
            lines.append(f"\n... و {len(results) - limit} سیگنال دیگر (فایل CSV پیوست است)")

        return "\n".join(lines)

    def send_results(self, results, limit=20):

        text = self.format_results(results, limit=limit)

        return self.send_message(text)
