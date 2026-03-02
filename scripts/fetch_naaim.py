import os
import io
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_naaim_exposure():
    print(f"[{datetime.now()}] 开始抓取 NAAIM 机构仓位数据...")
    
    base_url = "https://naaim.org/programs/naaim-exposure-index/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        # 1. 获取网页并解析下载链接
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        excel_link = None
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.endswith('.xlsx') and 'Data-since-Inception' in href:
                excel_link = href
                break
                
        if not excel_link:
            for a_tag in soup.find_all('a', href=True):
                if a_tag['href'].endswith('.xlsx'):
                    excel_link = a_tag['href']
                    break

        if not excel_link:
            raise ValueError("❌ 未找到 NAAIM Excel 下载链接！")
            
        print(f"✅ 成功解析到最新下载链接: {excel_link}")

        # 2. 下载并读取 Excel
        excel_response = requests.get(excel_link, headers=headers, timeout=15)
        excel_response.raise_for_status()
        
        df = pd.read_excel(io.BytesIO(excel_response.content))
        
        # ================= 数据清洗核心逻辑 =================
        
        # 1. 规范化列名 (原表有10列)
        df.columns = [
            'Date', 'Mean_Average', 'Most_Bearish', 'Quart_1', 
            'Median', 'Quart_3', 'Most_Bullish', 'Std_Dev', 
            'NAAIM_Number', 'SP500'
        ]
        
        # 2. 强制转换日期，并剔除底部的免责声明或空行
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        
        # 3. 按日期正序排列 (从老到新)，方便画图
        df = df.sort_values('Date')
        
        # ==================================================
        
        # 3. 保存为 CSV
        os.makedirs('data', exist_ok=True)
        file_path = 'data/naaim_exposure.csv'
        # 格式化日期为 YYYY-MM-DD
        df.to_csv(file_path, index=False, date_format='%Y-%m-%d')
        
        print(f"✅ NAAIM 数据抓取并清洗成功！已保存至 {file_path}，共 {len(df)} 行。")

    except Exception as e:
        print(f"❌ NAAIM 抓取失败: {e}")

if __name__ == "__main__":
    fetch_naaim_exposure()