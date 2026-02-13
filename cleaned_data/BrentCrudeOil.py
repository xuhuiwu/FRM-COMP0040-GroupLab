import yfinance as yf
import pandas as pd

# 1. 设定参数
# 链接中的 symbol 是 "BZ=F"
ticker = "BZ=F"  
start_date = "2020-01-01"
end_date = "2026-01-01"

print(f"正在下载布伦特原油期货 ({ticker}) ...")

# 2. 下载数据
# auto_adjust=False: 确保获取原始收盘价 (Close)，而不是调整后的价格
try:
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
    
    if df.empty:
        print("警告：下载的数据为空，请检查网络或代号。")
    else:
        print(f"下载成功！共获取 {len(df)} 行数据。")

        # 3. 数据清洗
        # 重命名索引为 observation_date
        df.index.name = 'observation_date'

        # 只保留收盘价 'Close'，并改名为 'Brent_Price'
        df_clean = df[['Close']].copy()
        df_clean.columns = ['Brent_Price']

        # 4. 填充缺失值 (关键步骤)
        # 将时间轴对齐到每个工作日 (Business Days)，把假期找回来变成 NaN
        df_clean = df_clean.asfreq('B')
        
        # 使用前向填充 (Forward Fill) 处理假期和空缺
        df_clean = df_clean.ffill()

        # 5. 保存文件
        output_file = 'brent_crude_cleaned.csv'
        # float_format='%.2f': 保留两位小数
        df_clean.to_csv(output_file, float_format='%.2f')

        print(f"\n清洗完成！文件已保存为: {output_file}")
        print("前5行预览：")
        print(df_clean.head())

except Exception as e:
    print(f"发生错误: {e}")