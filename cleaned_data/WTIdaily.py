import yfinance as yf
import pandas as pd

# 1. 设定参数
# CL=F 是 WTI Crude Oil Futures 的标准代码
ticker = "CL=F"
start_date = "2020-01-01"
end_date = "2026-01-01"
output_file = "wti_daily_cleaned.csv"

print(f"正在下载 WTI 原油期货 ({ticker}) ...")

try:
    # 2. 下载数据
    # auto_adjust=False: 确保获取原始收盘价
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)

    if df.empty:
        print("错误：下载数据为空，请检查网络或代码。")
    else:
        # 3. 数据清洗
        # 重命名索引
        df.index.name = 'observation_date'

        # 只保留收盘价，并重命名为 'WTI_Price'
        df_clean = df[['Close']].copy()
        df_clean.columns = ['WTI_Price']

        # 4. 填充假期 (关键)
        # 对齐到工作日 (Business Days)
        df_clean = df_clean.asfreq('B')
        # 前向填充
        df_clean = df_clean.ffill()

        # 5. 保存
        df_clean.to_csv(output_file, float_format='%.2f')

        print(f"\n成功！文件已保存为: {output_file}")
        print("前5行预览：")
        print(df_clean.head())

except Exception as e:
    print(f"发生错误: {e}")