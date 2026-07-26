from src.scanners import quant_engine
from src.scanners import quant_flow
from src.scanners import stock_engine
from src.scanners import stock_scanner_engine
from src.scanners import stock_alert_system
from src.utils.notifier import send_bark_notification
import datetime

def build_webpage(stocks_dict):
    """把股票字典畫成漂亮的網頁卡片"""
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if not stocks_dict:
        stock_html = "<div class='card empty'>今天沒有符合條件的股票 😴</div>"
    else:
        stock_html = ""
        for ticker, details in stocks_dict.items():
            # 把 Python 的換行 \n 變成網頁的換行 <br>
            html_details = details.replace('\n', '<br>')
            stock_html += f"<div class='card'>{html_details}</div>"

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Railway 掃描系統</title><style>
body {{ font-family: -apple-system, sans-serif; background: #f3f4f6; padding: 20px; margin: 0; }}
.container {{ max-width: 500px; margin: 0 auto; }}
h1 {{ text-align: center; color: #111827; font-size: 24px; margin-bottom: 5px; }}
.time {{ text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 20px; }}
.card {{ background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; font-size: 16px; line-height: 1.6; color: #1f2937; letter-spacing: 0.5px; font-weight: 500; }}
.card.empty {{ text-align: center; color: #6b7280; font-weight: normal; }}
</style></head>
<body><div class="container"><h1>🎯 Railway 掃描結果</h1><div class="time">最後更新：{time_str}</div>{stock_html}</div></body></html>"""
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html)
    print("🌐 網頁版 index.html 已生成！")

def main():
    # 建立一個大字典來裝所有結果
    all_stocks_dict = {}

    # 執行所有引擎，用 update() 魔法，如果有相同的股票代號(Key)，它會自動覆蓋去重複！
    try: all_stocks_dict.update(quant_engine.run())
    except: pass
    try: all_stocks_dict.update(quant_flow.run())
    except: pass
    try: all_stocks_dict.update(stock_engine.run())
    except: pass
    try: all_stocks_dict.update(stock_scanner_engine.run())
    except: pass
    try: all_stocks_dict.update(stock_alert_system.run())
    except: pass

    # 建立網頁
    build_webpage(all_stocks_dict)
    
    # 發送推播
    if len(all_stocks_dict) > 0:
        send_bark_notification(all_stocks_dict)

if __name__ == "__main__":
    main()
