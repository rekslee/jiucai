import os
import pandas as pd
from fredapi import Fred
from datetime import datetime

def fetch_employment_data():
    # 1. 从环境变量获取 API Key (绝对不要把明文 Key 写在代码里！)
    api_key = os.environ.get('FRED_API_KEY')
    if not api_key:
        raise ValueError("未找到 FRED_API_KEY 环境变量！")
    
    fred = Fred(api_key=api_key)
    print(f"[{datetime.now()}] 开始抓取 FRED 就业数据...")

    try:
        # 2. 抓取核心就业指标
        # ICSA: 初请失业金人数 (周更)
        # PAYEMS: 非农就业人数 (月更)
        # UNRATE: 失业率 (月更)
        icsa = fred.get_series('ICSA')
        payems = fred.get_series('PAYEMS')
        unrate = fred.get_series('UNRATE')

        # 3. 合并为一个 DataFrame
        df = pd.DataFrame({
            '初请失业金(ICSA)': icsa,
            '非农就业(PAYEMS)': payems,
            '失业率(UNRATE)': unrate
        })

        # 4. 数据清洗：按日期排序，只保留最近 10 年的数据 (保持文件轻量)
        df.index.name = 'Date'
        df = df.sort_index()
        
        # 获取10年前的年份
        ten_years_ago = str(datetime.now().year - 10)
        df = df.loc[ten_years_ago:] 

        # 5. 确保 data 文件夹存在
        os.makedirs('data', exist_ok=True)

        # 6. 保存为 CSV 文件 (直接覆盖)
        file_path = 'data/fred_employment.csv'
        df.to_csv(file_path)
        print(f"✅ 数据抓取成功！已保存至 {file_path}，共 {len(df)} 行数据。")

    except Exception as e:
        print(f"❌ 抓取失败: {e}")

if __name__ == "__main__":
    fetch_employment_data()