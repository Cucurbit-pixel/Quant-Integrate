import requests

TIER_SIGNALS = {"S": "🚀🚀🚀 強烈買入", "A": "🚀 買入", "B": "⚠️ 觀望", "C": "⚠️ 減碼", "D": "🚫 避免"}

def run():
    results = {}
    
    # 💡 魔法在這裡：指向你截圖裡面的 latest_scan.json
    json_url = "https://raw.githubusercontent.com/Cucurbit-pixel/Stock-scanner-engine/main/latest_scan.json"

    try:
        response = requests.get(json_url, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Stock-scanner-engine: 找不到 JSON，狀態碼 {response.status_code}")
            return results

        data = response.json()
        
        # 自動適應不同的 JSON 結構 (有時是字典，有時是列表)
        if isinstance(data, dict):
            candidates = data.get("top_candidates", data.get("results", []))
        elif isinstance(data, list):
            candidates = data
        else:
            candidates = []

        for c in candidates[:10]:
            ticker = c.get("ticker", c.get("symbol", "N/A"))
            if ticker == "N/A": continue
            
            tier = c.get("tier", "B")
            signal = TIER_SIGNALS.get(tier, TIER_SIGNALS["B"])
            
            # 安全地抓取數據並格式化
            rs_rating = c.get("rs_rating")
            rs_rating_label = f"{rs_rating:.0f}" if isinstance(rs_rating, (int, float)) else "N/A"
            
            rsi = c.get("rsi14", c.get("rsi"))
            rsi_label = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else "N/A"
            
            macd_label = c.get("macd_status", "⚪ 中性")
            trend_label = "多頭排列" if c.get("trend_ok", True) else "空頭排列"
            
            close = c.get("close", c.get("price", 0))
            entry = c.get("entry", float(close) * 0.995) if close else 0
            stop_loss = c.get("stop_loss", float(close) * 0.97) if close else 0
            take_profit = c.get("take_profit", float(close) * 1.05) if close else 0

            formatted_text = f"""Tier {tier}
📊 {ticker} (來自 Scanner-Engine)
{signal}
RS Rating : {rs_rating_label}
RSI: {rsi_label}
MACD: {macd_label}
趨勢：{trend_label}
現價 : ${float(close):.2f} | 入場 : ${float(entry):.2f}
止損 : ${float(stop_loss):.2f} | 止盈 : ${float(take_profit):.2f}"""

            results[ticker] = formatted_text

        print("✅ 成功下載並轉換 Stock-scanner-engine 數據！")

    except Exception as e:
        print(f"❌ Stock-scanner-engine 讀取 JSON 時發生錯誤: {e}")

    return results

