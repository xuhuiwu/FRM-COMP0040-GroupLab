import pandas as pd

# 1. 读取数据
# na_values=['.']: 这一步很关键。FRED 数据有时用 '.' 表示缺失，有时用空字符串。
# 加上这个参数，Pandas 会把 '.' 和空值都统一识别为 NaN。
df = pd.read_csv('sp500.csv', 
                 parse_dates=['observation_date'], 
                 index_col='observation_date',
                 na_values=['.']) 

# 打印一下看看 2020-01-20 是不是 NaN
print("清洗前 2020-01-20 的值:", df.loc['2020-01-20'])

# 2. 前向填充 (Forward Fill)
# 直接填补那些空值
df_clean = df.ffill()

# 3. 验证填充结果
print("\n--- 验证 2020-01-20 (马丁路德金日) ---")
# 应该看到 1月20日 的值变成了 1月17日(3329.62) 的值
print(df_clean.loc['2020-01-17':'2020-01-21'])

# 4. 保存
df_clean.to_csv('sp500_cleaned.csv', float_format='%.2f')
print("\n文件已保存！")