from src.scanners import quant_engine
from src.scanners import quant_flow
from src.scanners import stock_engine
from src.scanners import stock_scanner_engine
from src.scanners import stock_alert_system
from src.utils.notifier import send_bark_notification
import datetime

def build_webpage(stocks):
    """把股票名單畫成網頁"""
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    if not stocks:
        stock_html = "<li style='background:#f3f4f6; color:#6b7280; font-weight:normal;'>今天沒有符合條件的股票 😴</li>"
    else:
        stock_html = "".join([f"<li>📈 {s}</li>" for s in stocks])

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>臨玖的量化系統</title><style>body {{ font-family: -apple-system, sans-serif; background: #f3f4f6; padding: 20px; }}.box {{ max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}h1 {{ text-align: center; font-size: 24px; margin-bottom: 5px; }}ul {{ list-style: none; padding: 0; }}li {{ background: #eff6ff; color: #1d4ed8; padding: 15px; margin-bottom: 10px; border-radius: 8px; font-weight: bold; font-size: 18px; text-align: center; }}</style></head>
<body><div class="box"><h1>🎯 聯合掃描報告</h1><p style="text-align:center; color:#6b7280; font-size:14px; margin-bottom:20px;">最後更新：{time_str}</p><ul>{stock_html}</ul></div></body></html>"""
    
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html)
    print("🌐 網頁版 index.html 已生成！")

def main():
    all_stocks = []
    try: all_stocks.extend(quant_engine.run())
    except: pass
    try: all_stocks.extend(quant_flow.run())
    except: pass
    try: all_stocks.extend(stock_engine.run())
    except: pass
    try: all_stocks.extend(stock_scanner_engine.run())
    except: pass
    try: all_stocks.extend(stock_alert_system.run())
    except: pass

    unique_stocks = list(set(all_stocks))
    unique_stocks.sort()

    build_webpage(unique_stocks) # 觸發做網頁的功能
    
    if len(unique_stocks) > 0:
        send_bark_notification(unique_stocks)

if __name__ == "__main__":
    main()
