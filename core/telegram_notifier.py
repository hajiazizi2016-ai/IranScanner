import logging
import subprocess
import requests


def detect_psiphon_proxy(timeout=5):
    try:
        netstat = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=10).stdout
        tasklist = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=10).stdout
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
            if parts[-1] not in psiphon_pids:
                continue
            try:
                candidate_ports.append(int(parts[1].rsplit(":", 1)[1]))
            except (ValueError, IndexError):
                continue
        for port in candidate_ports:
            try:
                r = requests.get("https://api.telegram.org", proxies={"https": f"socks5h://127.0.0.1:{port}"}, timeout=timeout)
                if r.status_code == 200:
                    logging.info("پراکسی سایفون پیدا شد: %s", port)
                    return f"socks5h://127.0.0.1:{port}"
            except Exception:
                continue
        return None
    except Exception as e:
        logging.warning("خطا در تشخیص پراکسی سایفون: %s", e)
        return None


class TelegramNotifier:
    API_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token, chat_id, proxy=None):
        if not token or not chat_id:
            raise ValueError("Telegram token/chat_id تنظیم نشده.")
        self.token = token
        self.chat_id = chat_id
        self.proxies = {"http": proxy, "https": proxy} if proxy else None

    def send_message(self, text, parse_mode="HTML"):
        url = self.API_URL.format(token=self.token, method="sendMessage")
        chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)] or [""]
        ok = True
        for chunk in chunks:
            try:
                data = {"chat_id": self.chat_id, "text": chunk, "disable_web_page_preview": True}
                if parse_mode:
                    data["parse_mode"] = parse_mode
                resp = requests.post(url, data=data, proxies=self.proxies, timeout=15)
                if resp.status_code != 200:
                    logging.error("TELEGRAM ERROR: %s %s", resp.status_code, resp.text)
                    ok = False
            except Exception as e:
                logging.error("TELEGRAM SEND FAILED: %s", e, exc_info=True)
                ok = False
        return ok

    def send_file(self, file_path, caption=""):
        url = self.API_URL.format(token=self.token, method="sendDocument")
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(url, data={"chat_id": self.chat_id, "caption": caption}, files={"document": f}, proxies=self.proxies, timeout=30)
            if resp.status_code != 200:
                logging.error("TELEGRAM FILE ERROR: %s %s", resp.status_code, resp.text)
                return False
            return True
        except Exception as e:
            logging.error("TELEGRAM FILE SEND FAILED: %s", e, exc_info=True)
            return False

    def format_results(self, results, limit=20):
        if not results:
            return "امروز هیچ سیگنالی پیدا نشد. 🔍"
        lines = [f"📊 <b>نتایج اسکن امروز</b> — {len(results)} سیگنال\n"]
        for s in results[:limit]:
            symbol = getattr(s, "symbol", "")
            score = round(getattr(s, "final_score", getattr(s, "final_rank", 0)), 1)
            rr = round(getattr(s, "rr", 0), 2)
            rr_power = round(getattr(s, "rr_power", 0), 2)
            vol_ratio = round(getattr(s, "volume_ratio", 0), 2)
            buyer_power = round(getattr(s, "buyer_power", 0), 2)
            reason = getattr(s, "smart_money_reason", "") or getattr(s, "validation_reason", "")
            lines.append(f"🔹 <b>{symbol}</b> | امتیاز: {score}\n   RR: {rr} | قدرت RR: {rr_power} | حجم: {vol_ratio}x | قدرت خریدار: {buyer_power}\n   {reason}")
        if len(results) > limit:
            lines.append(f"\n... و {len(results) - limit} سیگنال دیگر (فایل CSV پیوست است)")
        return "\n".join(lines)

    def send_results(self, results, limit=20):
        return self.send_message(self.format_results(results, limit=limit))
