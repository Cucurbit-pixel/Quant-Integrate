import requests

TIER_SIGNALS = {
    "S": "🚀🚀🚀 強烈買入",
    "A": "🚀 買入",
    "B": "⚠️ 觀望",
    "C": "⚠️ 減碼",
    "D": "🚫 避免",
}
MACD_STATUS_LABELS = {
    "golden_cross": "🟢 MACD 金叉",
    "bullish_momentum": "🟢 多頭動能",
    "neutral": "⚪ 中性",
    "bearish_momentum": "🔴 空頭動能",
    "death_cross": "🔴 MACD 死叉",
    "insufficient_data": "⚪ 數據不足",
}

def run():
    results = {}
    
    # 👉 網址直接指向 QuantFlow 的 JSON
    json_url = "[https://raw.githubusercontent.com/Cucurbit-pixel/QuantFlow/main/output/final_candidates.json](https://raw.githubusercontent.com/Cucurbit-pixel/QuantFlow/main/output/final_candidates.json)"

    try:
        response = requests.get(json_url, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ QuantFlow: 找不到 JSON，狀態碼 {response.status_code}")
            return results

        data = response.json()
        candidates = data.get("top_candidates", [])[:10]

        for c in candidates:
            ticker = c.get("ticker", "N/A")
            tier = c.get("tier", "B")
            signal = TIER_SIGNALS.get(tier, TIER_SIGNALS["B"])

            rs_rating = c.get("rs_rating")
            rs_rating_label = f"{rs_rating:.0f}" if rs_rating is not None else "N/A"

            rsi = c.get("rsi14")
            rsi_label = f"{rsi:.1f}" if rsi is not None else "N/A"

            macd_status = c.get("macd_status", "neutral")
            macd_label = MACD_STATUS_LABELS.get(macd_status, "⚪ 中性")

            trend_label = "多頭排列" if c.get("trend_ok") else "空頭排列"

            close = c.get("close", 0)
            entry = c.get("entry", close * 0.995)
            stop_loss = c.get("stop_loss", close * 0.97)
            take_profit = c.get("take_profit", close * 1.05)
            off_52w = c.get("off_52w_high_pct", 0)

            # 💡 標題加入了 (QuantFlow)，方便你在網頁分辨來源！
            formatted_text = f"""Tier {tier}
📊 {ticker} (來自 QuantFlow)
{signal}
RS Rating : {rs_rating_label}
RSI: {rsi_label}
MACD: {macd_label}
趨勢：{trend_label}
距離52週新高：{off_52w:.1f}%
現價 : ${close:.2f} | 入場 : ${entry:.2f} | 止損 : ${stop_loss:.2f}
止盈 1 : ${take_profit:.2f}"""

            results[ticker] = formatted_text

        print("✅ 成功從舊專案下載並轉換 QuantFlow 數據！")

    except Exception as e:
        print(f"❌ QuantFlow 讀取 JSON 時發生錯誤: {e}")

    return results
