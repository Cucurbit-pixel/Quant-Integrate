# 引入剛才建立的 5 個引擎
from src.scanners import quant_engine
from src.scanners import quant_flow
from src.scanners import stock_engine
from src.scanners import stock_scanner_engine
from src.scanners import stock_alert_system

# 引入推播功能
from src.utils.notifier import send_bark_notification

def main():
    all_stocks = []

    print("🔍 開始執行 5 大美股引擎...")

    # 1. 執行 Quant-Engine
    try:
        all_stocks.extend(quant_engine.run())
    except Exception as e:
        print(f"Quant-Engine 錯誤: {e}")

    # 2. 執行 QuantFlow
    try:
        all_stocks.extend(quant_flow.run())
    except Exception as e:
        print(f"QuantFlow 錯誤: {e}")

    # 3. 執行 Stock-Engine
    try:
        all_stocks.extend(stock_engine.run())
    except Exception as e:
        print(f"Stock-Engine 錯誤: {e}")

    # 4. 執行 Stock-Scanner-Engine
    try:
        all_stocks.extend(stock_scanner_engine.run())
    except Exception as e:
        print(f"Stock-Scanner-Engine 錯誤: {e}")

    # 5. 執行 stock-alert-system
    try:
        all_stocks.extend(stock_alert_system.run())
    except Exception as e:
        print(f"stock-alert-system 錯誤: {e}")

    # 目前 all_stocks 裡面包含所有股票 (包含重複的)
    print(f"原始收集到的股票: {all_stocks}")
    
    # 施展魔法：過濾重複！用 set() 把它變成沒有重複的集合
    unique_stocks = list(set(all_stocks))
    
    # 幫股票按照英文字母排個序，比較好看
    unique_stocks.sort()
    
    print(f"最終過濾後的股票: {unique_stocks}")

    # 如果有股票，就發送到手機 Bark
    if len(unique_stocks) > 0:
        send_bark_notification(unique_stocks)
    else:
        print("今天沒有符合條件的股票。")

if __name__ == "__main__":
    main()
