import yfinance as yf
import pandas as pd

# 1. 设定参数
ticker = "^OVX"  # CBOE Crude Oil Volatility Index
start_date = "2020-01-01"
end_date = "2026-01-01"

print(f"正在下载原油波动率指数 ({ticker})...")

# 2. 下载数据
# auto_adjust=False: 保持原始收盘价
df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

# 3. 格式化清洗
# 将索引重命名为 observation_date
df.index.name = 'observation_date'

# 只保留收盘价
df_clean = df[['Close']].copy()

# 重命名列: 建议叫 OVX_Close 或 Oil_Volatility
df_clean.columns = ['OVX_Close']

# 4. 填充假期 (Forward Fill)
# 波动率指数也是金融时间序列，需要对齐到工作日并填充假期
df_clean = df_clean.asfreq('B')  # 扩展为所有工作日
df_clean = df_clean.ffill()

# 5. 保存
filename = "ovx.csv"
# OVX 是百分比读数（如 35.50），保留两位小数即可
df_clean.to_csv(filename, float_format='%.2f')

print(f"下载成功！文件已保存为: {filename}")
print("\n--- 数据预览 ---")
print(df_clean.tail())