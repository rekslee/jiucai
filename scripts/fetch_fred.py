import os
import pandas as pd
from fredapi import Fred
from datetime import datetime

def fetch_all_macro_data():
    # 1. 获取 API Key
    api_key = os.environ.get('FRED_API_KEY')
    if not api_key:
        raise ValueError("未找到 FRED_API_KEY 环境变量！")
    
    fred = Fred(api_key=api_key)
    print(f"[{datetime.now()}] 开始抓取 FRED 宏观全量历史数据...")

    # 2. 定义要抓取的指标字典 (按类别分组)
    # 字典格式: {"保存的文件名": {"列名": "FRED的Ticker代码"}}
    indicators = {
        "employment": {
            "初请失业金(ICSA)": "ICSA",
            "非农就业(PAYEMS)": "PAYEMS",
            "失业率(UNRATE)": "UNRATE"
        },
        "consumption": {
            "个人储蓄率(PSAVERT)": "PSAVERT",
            "零售销售额(RSAFS)": "RSAFS"
        },
        "housing": {
            "新屋销售(HSN1F)": "HSN1F",
            "现房销售(EXHOSLUSM495S)": "EXHOSLUSM495S",
            "房价指数(CSUSHPISA)": "CSUSHPISA",
            "建筑许可(PERMIT)": "PERMIT"
        },
        "inflation": {
            "CPI(CPIAUCSL)": "CPIAUCSL",
            "核心CPI(CPILFESL)": "CPILFESL",
            "核心PCE(PCEPILFE)": "PCEPILFE"
        },
        "financial": {
            "纽约联储WEI(WEI)": "WEI",
            "CCC级信用利差(BAMLH0A3HYC)": "BAMLH0A3HYC"
        }
    }

    # 3. 确保 data 文件夹存在
    os.makedirs('data', exist_ok=True)

    # 4. 循环抓取并分类保存
    for category, series_dict in indicators.items():
        print(f"\n⏳ 正在抓取类别: {category} ...")
        df_dict = {}
        
        for col_name, ticker in series_dict.items():
            try:
                # 获取全量历史数据
                series_data = fred.get_series(ticker)
                df_dict[col_name] = series_data
                print(f"  - 成功获取: {col_name} (自 {series_data.index.min().strftime('%Y-%m-%d')} 起)")
            except Exception as e:
                print(f"  ❌ 获取失败: {col_name} ({ticker}) - 错误: {e}")
        
        # 如果该类别下有数据，则合并并保存为 CSV
        if df_dict:
            df = pd.DataFrame(df_dict)
            df.index.name = 'Date'
            df = df.sort_index() # 按日期升序排列
            
            file_path = f'data/fred_{category}.csv'
            df.to_csv(file_path)
            print(f"✅ {category} 数据已保存至 {file_path}，共 {len(df)} 行。")

if __name__ == "__main__":
    fetch_all_macro_data()