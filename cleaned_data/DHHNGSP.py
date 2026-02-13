import pandas as pd
import numpy as np

# 1. 读取数据
# na_values=['.']: FRED 的数据经常用一个点 "." 来表示缺失，必须告诉 pandas 把它当成 NaN 处理
# parse_dates=True: 自动解析日期
# index_col=0: 把日期列作为索引
input_file = 'DHHNGSP.csv'
output_file = 'DHHNGSP_cleaned.csv'

print(f"正在读取 {input_file} ...")

try:
    df = pd.read_csv(input_file, 
                     parse_dates=True, 
                     index_col=0, 
                     na_values=['.']) # 关键：把 "." 识别为 NaN
except FileNotFoundError:
    print(f"错误：找不到文件 {input_file}，请检查文件名。")
    exit()

# 重命名列，方便后续引用
df.columns = ['Gas_Price']

# 2. 强制对齐到工作日 (Business Days)
# 这一步会把像 2021-02-15 (总统日) 这种原本可能不存在的日期行，强制加进来（值为 NaN）
df_expanded = df.asfreq('B')

# 3. 前向填充 (Forward Fill)
# 用前一天的价格填补假期
df_clean = df_expanded.ffill()

# -------------------------------------------------------
# 4. 验证关键节点 (您提到的 2021年2月 寒潮)
# -------------------------------------------------------
print("\n--- 验证：2021年2月 德州寒潮期间数据 ---")
check_dates = ['2021-02-12', '2021-02-15', '2021-02-16', '2021-02-17']
for date in check_dates:
    try:
        price = df_clean.loc[date, 'Gas_Price']
        print(f"{date}: {price:.2f}")
    except KeyError:
        print(f"{date}: 数据缺失")

# 5. 保存文件
# float_format='%.2f': 保留两位小数
df_clean.to_csv(output_file, float_format='%.2f')

print(f"\n成功！清洗后的文件已保存为: {output_file}")
print(f"总行数: {len(df_clean)}")