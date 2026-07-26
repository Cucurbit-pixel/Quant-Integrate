import requests
import os
from urllib.parse import quote

def send_bark_notification(stocks_list):
    bark_key = os.getenv("BARK_KEY")
    if not bark_key:
        print("找不到 Bark Key，無法發送推播。")
        return

    # 把 ["AAPL", "NVDA"] 變成 "AAPL, NVDA"
    stock_str = ", ".join(stocks_list)
    title = quote("🎯 美股聯合掃描結果")
    content = quote(f"今日符合條件的標的：\n{stock_str}")
    
    url = f"[https://api.day.app/](https://api.day.app/){bark_key}/{title}/{content}"
    
    try:
        requests.get(url)
        print("✅ 成功發送推播到 iPhone！")
    except:
        print("❌ 推播發送失敗")
