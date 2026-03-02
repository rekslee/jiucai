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
    
    # 1. 构造下载链接
    urls = [
        # CFTC 官方提供的 1986-2016 历史汇总包
        "https://www.cftc.gov/files/dea/history/deacot1986_2016.zip"
    ]
    
    # 加上 2017 年至今的年度包
    current_year = datetime.now().year
    for year in range(2017, current_year + 1):
        urls.append(f"https://www.cftc.gov/files/dea/history/deacot{year}.zip")
        
    # 2. 循环下载并在内存中解压读取
    for url in urls:
        print(f"⏳ 正在下载: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    # 找到压缩包里的 txt 或 csv 数据文件
                    data_files = [f for f in z.namelist() if f.endswith('.txt') or f.endswith('.csv')]
                    if data_files:
                        with z.open(data_files[0]) as f:
                            # CFTC 数据是逗号分隔的
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
        
    # 3. 合并所有年份的数据
    df_all = pd.concat(df_list, ignore_index=True)
    
    # 4. 数据清洗
    df_all.columns = df_all.columns.str.strip()
    
    # 提取核心列：品种、日期、投机多头(Non-Commercial Long)、投机空头(Non-Commercial Short)
    cols_to_keep = [
        'Market and Exchange Names',
        'Report_Date_as_YYYY-MM-DD',
        'NonComm_Positions_Long_All',
        'NonComm_Positions_Short_All'
    ]
    
    df_clean = df_all[cols_to_keep].copy()
    df_clean.rename(columns={
        'Market and Exchange Names': 'Market',
        'Report_Date_as_YYYY-MM-DD': 'Date',
        'NonComm_Positions_Long_All': 'Spec_Long',
        'NonComm_Positions_Short_All': 'Spec_Short'
    }, inplace=True)
    
    # 计算净投机仓位 (Net Speculative Position = 多头 - 空头)
    df_clean['Net_Spec_Position'] = df_clean['Spec_Long'] - df_clean['Spec_Short']
    
    # 转换日期格式并剔除空值
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
    df_clean = df_clean.dropna(subset=['Date'])
    
    # 5. 过滤核心宏观品种 (使用模糊匹配，防止 CFTC 更改后缀名)
    # 你可以在这里自由添加你关注的品种关键词
    keywords = {
        'GOLD -': 'Gold',                                  # 黄金
        'CRUDE OIL, LIGHT SWEET': 'Crude Oil',             # WTI原油
        'E-MINI S&P 500': 'S&P 500',                       # 标普500
        '10-YEAR U.S. TREASURY NOTES': '10Y Treasury',     # 10年期美债
        'EURO FX': 'Euro'                                  # 欧元
    }
    
    filtered_dfs = []
    for keyword, short_name in keywords.items():
        temp_df = df_clean[df_clean['Market'].str.contains(keyword, case=False, na=False)].copy()
        temp_df['Market'] = short_name
        filtered_dfs.append(temp_df)
        
    df_filtered = pd.concat(filtered_dfs, ignore_index=True)
    
    # 去重并按品种和日期排序 (从老到新)
    df_filtered = df_filtered.drop_duplicates(subset=['Market', 'Date'])
    df_filtered = df_filtered.sort_values(['Market', 'Date'])
    
    # 6. 保存为 CSV
    os.makedirs('data', exist_ok=True)
    file_path = 'data/cftc_cot.csv'
    df_filtered.to_csv(file_path, index=False, date_format='%Y-%m-%d')
    
    print(f"✅ CFTC COT 数据抓取并清洗成功！已保存至 {file_path}，共 {len(df_filtered)} 行。")

if __name__ == "__main__":
    fetch_cftc_cot()