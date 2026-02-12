import pandas as pd

# 1. 读取数据
# parse_dates: 自动解析日期列
# index_col: 将日期列设为索引
# na_values: FRED 数据常将假期标记为 '.'，我们需要将其识别为 NaN 才能填充
df = pd.read_csv('T10YIE.csv', 
                 parse_dates=['observation_date'], 
                 index_col='observation_date', 
                 na_values=['.', 'NaN'])

# 打印填充前的状态（可选）
print(f"原始数据行数: {len(df)}")
print(f"包含的缺失值 (NaN) 数量:\n{df.isna().sum()}")

# -------------------------------------------------------
# 2. 核心步骤：Forward Fill (前向填充)
# -------------------------------------------------------
# inplace=False 默认创建新副本，避免修改原始 df
df_clean = df.ffill()

# 如果开头就是缺失值（ffill 填补不了），可以用 bfill (后向填充) 兜底
df_clean = df_clean.bfill()

# -------------------------------------------------------
# 3. 验证与保存
# -------------------------------------------------------

# 验证：打印 2003-01-20 (马丁路德金日) 前后的数据查看效果
# 使用 try-except 防止您的文件中正好没有这段时间的数据而报错
try:
    check_date = '2003-01-20'
    start = pd.Timestamp(check_date) - pd.Timedelta(days=5)
    end = pd.Timestamp(check_date) + pd.Timedelta(days=5)
    print(f"\n--- 验证日期: {check_date} 前后填充情况 ---")
    print(df_clean.loc[start:end])
except KeyError:
    print("\n数据中未找到 2003-01-20 附近的数据，跳过验证显示。")

# 保存为新文件
output_filename = 'T10YIE_cleaned.csv'
df_clean.to_csv(output_filename, float_format='%.2f')

print(f"\n清洗完成！文件已保存为: {output_filename}")