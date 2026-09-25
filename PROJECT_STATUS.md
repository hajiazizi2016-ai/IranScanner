# IranScanner - وضعیت پروژه (به‌روز)

## هدف پروژه
اسکن روزانه‌ی خودکار بازار بورس ایران (فقط سهام عادی)، امتیازدهی بر اساس
فیلتر «آتش زیر خاکستر» (RR/RR_Power) + فاکتورهای Smart Money، و ارسال
خودکار نتایج به تلگرام و ایمیل.

## وضعیت: ✅ کاملاً کاری (تاریخ آخرین تأیید: کاربر گفت "تمام همه چی عالیه")

## معماری
```
market_api.py      -> دریافت لحظه‌ای کل بازار (MarketWatchInit.aspx)
history_downloader.py -> تاریخچه قیمت هر نماد (InstTradeHistory.aspx)
client_type_history_downloader.py -> تاریخچه حقیقی/حقوقی هر نماد (clienttype.aspx)
data_provider.py   -> فیلتر "فقط سهام" (is_stock) + پاکسازی
engine.py           -> محاسبه اندیکاتورها + Smart Money + امتیازدهی نهایی
ranking.py           -> رتبه‌بندی نهایی
daily_runner.py     -> اجرای کامل روزانه + ارسال تلگرام/ایمیل
```

## نحوه اجرا
- دستی: `py daily_runner.py`
- خودکار روی سیستم شخصی: Task Scheduler (اسم تسک: `IranScanner Daily`, ساعت ۱۲ ظهر)
  ⚠️ سیستم باید روشن/لاگین باشه، و سایفون هم وصل باشه (برای تلگرام)
- خودکار روی گیت‌هاب: `.github/workflows/daily.yml` ساخته شده ولی هنوز
  استفاده نمی‌شه چون **TSETMC از IPهای خارج از ایران بلاک می‌کنه** —
  برای همین فعلاً باید از سیستم ایرانی (شخصی یا VPS ایرانی) اجرا بشه

## کانال‌های اطلاع‌رسانی
- تلگرام: فعال (`config/telegram.json`) - نیاز به سایفون/VPN (چون تلگرام در ایران فیلتره)
  - پورت سایفون به‌صورت خودکار پیدا می‌شه (`detect_psiphon_proxy` در `telegram_notifier.py`)
- ایمیل: فعال (`config/email.json`) - Gmail SMTP، نیازی به VPN نداره

## باگ‌های رفع‌شده (تاریخچه کامل)
۱. جداکننده اشتباه در دانلود تاریخچه قیمت (`,` باید `;`/`@` می‌بود)
۲. ناسازگاری دیکشنری/لیست در `indicators.py`, `order_block.py`, `liquidity_grab.py`
۳. متدهای گمشده `kh_3_10`, `sarane3_10`, `haghighi_buy_average`, `sarane_average`
۴. `buyer_power` هیچ‌وقت محاسبه نمی‌شد
۵. `history_engine.py` فقط تاریخچه‌ی یک نماد (`symbols[0]`) دانلود می‌کرد، نه همه
۶. `final_score` در `ranking.py` هیچ‌وقت ست نمی‌شد
۷. حجم و تعداد معاملات در `market_parser.py` جابه‌جا بودن (f[8]/f[9])
۸. `cache_seconds` خیلی کوتاه بود (۳۰ ثانیه) و باعث ۲-۳ بار دانلود کامل بازار در هر اجرا می‌شد
۹. عدم وجود دانلودر تاریخچه‌ی حقیقی/حقوقی (KH/Sarane همیشه صفر بودن) - ساخته شد
۱۰. فیلتر «فقط سهام» اضافه شد (حذف اختیار معامله، حق تقدم، صندوق، اوراق و...)

## کارهای پاک‌شده (کد مرده، دیگه وجود ندارن)
`relative_strength.py`, `unusual_volume.py`, `trend.py`, `indicator_engine.py`,
`market_filter.py`, `stock_filter.py`, `symbol_api.py`, `support_resistance.py`,
`cache.py`, `dashboard.py`, `data_fetcher.py`, `db.py`, `instrument_loader.py`,
`liquidity.py`, `marketwatch_mapper.py`, `marketwatch_parser.py`, `parser.py`,
`raw_adapter.py`, `scoring.py`, `universe.py`, `database.py`, پوشه `tsetmc-api/`

## قدم‌های بعدی که هنوز انجام نشده (پیشنهادی، نه اجباری)
- سرور مجازی ایرانی (VPS) برای اجرای کاملاً مستقل از سیستم شخصی
  (چون GitHub Actions به خاطر بلاک بودن TSETMC از خارج جواب نداد)
- محدود کردن اعداد غیرعادی مثل BuyerPower خیلی بزرگ (مثلاً کاما۳: ۱۱۳۶۳۶)
- به‌روزرسانی `adaptive_score.py` / `config/weights.json` (فعلاً استفاده محدودی دارن)

## نکته امنیتی
توکن‌های واقعی تلگرام/ایمیل هرگز نباید در گیت‌هاب کامیت بشن (`.gitignore`
از این کار جلوگیری می‌کنه). نسخه‌ی نمونه: `config/*.json.example`
