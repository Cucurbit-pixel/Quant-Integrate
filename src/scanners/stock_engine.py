import requests

def run():
    results = {}
    
    # 指向舊專案產生出來的新 JSON
    json_url = "https://raw.githubusercontent.com/Cucurbit-pixel/Stock-Engine/main/output/final_candidates.json"

    try:
        response = requests.get(json_url, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️ Stock-Engine: 找不到 JSON，狀態碼 {response.status_code}")
            return results

        data = response.json()
        candidates = data.get("top_candidates", [])

        for c in candidates:
            # 抓取 AI 產生的資料
            ticker = c.get("ticker", "N/A")
            rs_rating = c.get("final_rs_str", "N/A")
            strength = c.get("recommendation_strength", "🚀 建議買入")
            action = c.get("action", "觀望")
            price = c.get("current_price", "N/A")
            buy = c.get("buy_price", "N/A")
            sell = c.get("sell_price", "N/A")
            
            # 提取 AI 的一句話點評
            tech_analysis = c.get("technical_analysis", "無分析")
            news_analysis = c.get("news_analysis", "無新聞簡評")

            # 🔮 AI 專屬精美排版！
            formatted_text = f"""🤖 AI 深度分析 (Stock-Engine)
📊 {ticker}
{strength} ({action})
RS 評分 : {rs_rating}
現價 : {price} | 入場 : {buy} | 止盈 : {sell}
💡 技術點評：{tech_analysis}
📰 消息簡評：{news_analysis}"""

            results[ticker] = formatted_text

        print("✅ 成功下載並轉換 Stock-Engine (AI) 數據！")

    except Exception as e:
        print(f"❌ Stock-Engine 讀取 JSON 時發生錯誤: {e}")

    return results

