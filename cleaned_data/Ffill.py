import pandas as pd
import os

# ================= 配置区域 =================
# 只需要改这里的文件名
input_file = 'DTWEXBGS.csv'   # 你的原始文件
output_file = 'DTWEXBGS_cleaned.csv' # 例如: 你清洗后的文件
# ===========================================

print(f"正在读取 {input_file} ...")

if not os.path.exists(input_file):
    print(f"错误：找不到文件 {input_file}")
    exit()

try:
    # 1. 读取数据
    # na_values=['.']: 专门处理 FRED 数据里的 "." 缺失值
    # index_col=0: 默认第一列是日期
    df = pd.read_csv(input_file, parse_dates=True, index_col=0, na_values=['.'])

    # 2. 强制对齐到工作日 (Business Days)
    # 这会把原本缺失的假期（如圣诞节）加回来变成空行
    df_clean = df.asfreq('B')

    # 3. 前向填充 (Forward Fill)
    # 核心步骤：用前一天的数据填补假期
    df_clean = df_clean.ffill()

    # 4. 保存
    # float_format='%.4f': 统一保留四位小数，看起来整洁
    df_clean.to_csv(output_file, float_format='%.4f')

    print(f"成功！已保存为: {output_file}")
    print(f"包含列名: {df_clean.columns.tolist()}")
    print("前3行预览：")
    print(df_clean.head(3))

except Exception as e:
    print(f"发生错误: {e}")