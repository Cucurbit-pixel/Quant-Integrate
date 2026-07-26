def run():
    # 這裡放你的真實運算邏輯...
    # 假設算出來是 MPC 還有 AAPL
    
    # 寫法教學：使用三個引號 """ 可以讓你自由地換行排版！
    mpc_text = """Tier S
📊 MPC
(Marathon Petroleum Corporation)
🚀🚀🚀強烈買入
RS Rating : 95
RSI: 50.0
MACD: bullish momentum
趨勢：多頭排列
距離52週新高：-1.9%
突破：一 無明顯突破
現價 : $313.81 | 入場 : $312.24 | 止損 : $304.4
止盈 1 : $xxx.xx | 止盈 2 : $xxx.xx | 止盈 3 : $xxx.xx"""

    # 最後，回傳一個字典 (Dictionary)
    # 左邊的 "MPC" 是給 main.py 去重複用的代碼
    # 右邊的 mpc_text 是給網頁跟推播顯示的排版
    return {
        "MPC": mpc_text
    }
