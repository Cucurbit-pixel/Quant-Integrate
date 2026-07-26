import requests

TIER_SIGNALS = {"S": "🚀🚀🚀 強烈買入", "A": "🚀 買入", "B": "⚠️ 觀望", "C": "⚠️ 減碼", "D": "🚫 避免"}

def run():
    results = {}
    
    # 指向舊專案產生出來的新 JSON
    json_url = "https://raw.githubusercontent.com/Cucurbit-pixel/stock-alert-system/main/output/final_candidates.json"

    try:
        response = requests.get(json_url, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Stock-alert-system: 找不到 JSON，狀態碼 {response.status_code}")
            return results

        data = response.json()
        candidates = data.get("top_candidates", [])

        for c in candidates:
            # 抓取資料
            ticker = c.get("ticker", "N/A")
            tier = c.get("tier", "S")
            signal = TIER_SIGNALS.get(tier, TIER_SIGNALS["B"])

            rs_rating = c.get("rs_rating")
            rs_rating_label = f"{rs_rating:.0f}" if rs_rating is not None else "N/A"

            rsi = c.get("rsi14")
            rsi_label = f"{rsi:.1f}" if rsi is not None else "N/A"

            macd_label = c.get("macd_status", "⚪ 中性")
            trend_label = "多頭排列" if c.get("trend_ok") else "空頭排列"

            close = c.get("close", 0)
            entry = c.get("entry", close * 0.995)
            stop_loss = c.get("stop_loss", close * 0.97)
            take_profit = c.get("take_profit", close * 1.05)
            
            # 💡 專屬 Kelly 倉位數據
            kelly_pct = c.get("kelly_pct", 0)

            # 🔮 專屬精美排版！
            formatted_text = f"""Tier {tier}
📊 {ticker} (來自 Alert-System)
{signal}
RS Rating : {rs_rating_label}
RSI: {rsi_label}
MACD: {macd_label}
趨勢：{trend_label}
💰 建議倉位：{kelly_pct}% (Kelly公式)
現價 : ${close:.2f} | 入場 : ${entry:.2f} | 止損 : ${stop_loss:.2f}
止盈 1 : ${take_profit:.2f}"""

            results[ticker] = formatted_text

        print("✅ 成功下載並轉換 Stock-alert-system 數據！")

    except Exception as e:
        print(f"❌ Stock-alert-system 讀取 JSON 時發生錯誤: {e}")

    return results

