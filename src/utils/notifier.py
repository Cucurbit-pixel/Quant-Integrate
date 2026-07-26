import requests
import os
from urllib.parse import quote

def send_bark_notification(stocks_dict):
    bark_key = os.getenv("BARK_KEY")
    if not bark_key:
        return

    # 將所有股票的詳細資訊合併，中間用虛線隔開
    content_list = []
    for ticker, details in stocks_dict.items():
        content_list.append(details)
    
    # 組合推播文字
    full_content = "\n\n➖➖➖➖➖➖➖➖\n\n".join(content_list)
    
    # 設定標題與內容
    title = quote("🎯 Railway掃描結果")
    content = quote(full_content)
    
    url = f"[https://api.day.app/](https://api.day.app/){bark_key}/{title}/{content}"
    
    try:
        requests.get(url)
        print("✅ 專業版推播已發送！")
    except:
        print("❌ 推播發送失敗")
