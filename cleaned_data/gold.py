import yfinance as yf
import pandas as pd

# 1. 设定参数
ticker = "GC=F"  # 纽约金 (COMEX Gold Futures)
start_date = "2020-01-01"
end_date = "2026-01-01"

print(f"正在通过 Yahoo Finance 下载 {ticker} ...")

# 2. 下载数据
# auto_adjust=False 确保我们拿到的是原始收盘价
df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

# 3. 格式化清洗
# 将索引重命名为 observation_date 以匹配您的其他文件
df.index.name = 'observation_date'

# 只保留收盘价，并重命名为 Gold_Price
df_clean = df[['Close']].copy()
df_clean.columns = ['Gold_Price']

# 4. 填充假期 (Forward Fill)
# 金融期货也有节假日，必须填充以保持时间序列连续
df_clean = df_clean.asfreq('B')  # 对齐到工作日
df_clean = df_clean.ffill()

# 5. 保存
filename = "gold.csv"
df_clean.to_csv(filename, float_format='%.2f')

print(f"下载成功！文件已保存为: {filename}")
print("前5行预览：")
print(df_clean.head())