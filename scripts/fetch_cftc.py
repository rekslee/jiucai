import os
import io
import requests
import zipfile
import pandas as pd
from datetime import datetime

def fetch_cftc_cot():
    print(f"[{datetime.now()}] 开始抓取 CFTC COT 投机仓位全量历史数据...")
    
    df_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    urls = [
        "https://www.cftc.gov/files/dea/history/deacot1986_2016.zip"
    ]
    
    current_year = datetime.now().year
    for year in range(2017, current_year + 1):
        urls.append(f"https://www.cftc.gov/files/dea/history/deacot{year}.zip")
        
    for url in urls:
        print(f"⏳ 正在下载: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    data_files = [f for f in z.namelist() if f.endswith('.txt') or f.endswith('.csv')]
                    if data_files:
                        with z.open(data_files[0]) as f:
                            df_year = pd.read_csv(f, low_memory=False)
                            df_list.append(df_year)
                print(f"  ✅ 下载并解析成功！")
            else:
                print(f"  ❌ 下载失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"  ❌ 下载出错: {e}")
            
    if not df_list:
        print("❌ 所有数据均下载失败！")
        return
        
    df_all = pd.concat(df_list, ignore_index=True)
    df_all.columns = df_all.columns.str.strip()
    
    # 👇 这里修复了列名，使用了 CFTC Legacy 报告的真实列名
    cols_to_keep = [
        'Market and Exchange Names',
        'As of Date in Form YYYY-MM-DD',
        'Noncommercial Positions-Long (All)',
        'Noncommercial Positions-Short (All)'
    ]
    
    try:
        df_clean = df_all[cols_to_keep].copy()
    except KeyError as e:
        print(f"❌ 找不到指定的列名！当前文件包含的列名有: {list(df_all.columns)[:10]}...")
        raise e
        
    df_clean.rename(columns={
        'Market and Exchange Names': 'Market',
        'As of Date in Form YYYY-MM-DD': 'Date',
        'Noncommercial Positions-Long (All)': 'Spec_Long',
        'Noncommercial Positions-Short (All)': 'Spec_Short'
    }, inplace=True)
    
    df_clean['Net_Spec_Position'] = df_clean['Spec_Long'] - df_clean['Spec_Short']
    
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
    df_clean = df_clean.dropna(subset=['Date'])
    
    keywords = {
        'GOLD -': 'Gold',
        'CRUDE OIL, LIGHT SWEET': 'Crude Oil',
        'E-MINI S&P 500': 'S&P 500',
        '10-YEAR U.S. TREASURY NOTES': '10Y Treasury',
        'EURO FX': 'Euro'
    }
    
    filtered_dfs = []
    for keyword, short_name in keywords.items():
        temp_df = df_clean[df_clean['Market'].str.contains(keyword, case=False, na=False)].copy()
        temp_df['Market'] = short_name
        filtered_dfs.append(temp_df)
        
    df_filtered = pd.concat(filtered_dfs, ignore_index=True)
    
    df_filtered = df_filtered.drop_duplicates(subset=['Market', 'Date'])
    df_filtered = df_filtered.sort_values(['Market', 'Date'])
    
    os.makedirs('data', exist_ok=True)
    file_path = 'data/cftc_cot.csv'
    df_filtered.to_csv(file_path, index=False, date_format='%Y-%m-%d')
    
    print(f"✅ CFTC COT 数据抓取并清洗成功！已保存至 {file_path}，共 {len(df_filtered)} 行。")

if __name__ == "__main__":
    fetch_cftc_cot()