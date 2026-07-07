class Dashboard:

    def __init__(self):
        print("Dashboard initialized")

    def build(self, watchlist):
        print("Building trading dashboard...")

        if not watchlist:
            return {
                "top": [],
                "message": "No strong signals today"
            }

        # مرتب‌سازی بر اساس قدرت سیگنال
        sorted_list = sorted(watchlist, key=lambda x: x["score"], reverse=True)

        top_5 = sorted_list[:5]

        return {
            "top_watchlist": top_5,
            "count": len(watchlist),
            "message": "Active trading opportunities detected"
        }