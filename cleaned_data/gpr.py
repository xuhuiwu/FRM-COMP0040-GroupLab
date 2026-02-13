import pandas as pd
import os

# 1. 设定文件名
input_file = 'gpr_daily.xls'
output_basic = 'gpr_daily_cleaned.csv'      # 文件1：只有 GPRD
output_detailed = 'gpr_detailed_cleaned.csv' # 文件2：GPRD + ACT + THREAT

print(f"正在读取 {input_file} ...")

if not os.path.exists(input_file):
    print(f"错误：找不到文件 {input_file}。请确保它在当前目录下。")
    exit()

try:
    # 2. 读取 Excel (使用 xlrd 引擎)
    df = pd.read_excel(input_file, engine='xlrd')

    # 3. 提取所有需要的列 (根据您的截图)
    # 第6列(索引5): date (日期)
    # 第3列(索引2): GPRD (总指数)
    # 第4列(索引3): GPRD_ACT (行动)
    # 第5列(索引4): GPRD_THREAT (威胁)
    
    # 我们先提取这 4 列
    df_subset = df.iloc[:, [5, 2, 3, 4]].copy()
    
    # 重命名为标准格式
    df_subset.columns = ['observation_date', 'GPR_Index', 'GPR_Acts', 'GPR_Threats']
    
    # 4. 数据清洗 (通用步骤)
    # 转为 datetime 格式
    df_subset['observation_date'] = pd.to_datetime(df_subset['observation_date'])
    
    # 设置索引
    df_subset.set_index('observation_date', inplace=True)
    df_subset.sort_index(inplace=True)

    # 截取时间范围 (2020-2026)
    target_start = "2020-01-01"
    target_end = "2026-01-01"
    df_clean = df_subset.loc[target_start:target_end].copy()

    # 填充假期 (对齐到工作日)
    df_clean = df_clean.asfreq('B')
    df_clean = df_clean.ffill()

    # -------------------------------------------------------
    # 5. 生成第一份数据：只有 GPR_Index
    # -------------------------------------------------------
    df_basic = df_clean[['GPR_Index']].copy()
    df_basic.to_csv(output_basic, float_format='%.2f')
    print(f"\n[1/2] 基础数据已保存: {output_basic}")
    print(df_basic.head(3))

    # -------------------------------------------------------
    # 6. 生成第二份数据：包含 Acts 和 Threats
    # -------------------------------------------------------
    # df_clean 本身就已经包含了这三列，直接保存即可
    df_clean.to_csv(output_detailed, float_format='%.2f')
    print(f"\n[2/2] 详细数据已保存: {output_detailed}")
    print(df_clean.head(3))

    print(f"\n全部完成！时间范围: {df_clean.index.min().date()} 到 {df_clean.index.max().date()}")

except Exception as e:
    print(f"\n发生错误: {e}")