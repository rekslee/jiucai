import os
import io
import requests
import pandas as pd
from datetime import datetime

def fetch_aaii_sentiment():
    print(f"[{datetime.now()}] 开始抓取 AAII 散户情绪数据...")
    
    # AAII 固定的下载链接 (注意是 .xls 格式)
    url = "https://www.aaii.com/files/surveys/sentiment.xls"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.aaii.com/sentimentsurvey',
        'Connection': 'keep-alive'
    }

    try:
        # 1. 下载 Excel 文件
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 2. 读取 Excel（不使用默认表头，直接读取所有数据）
        # 注意：因为是 .xls 文件，pandas 底层会使用 xlrd 引擎
        df = pd.read_excel(io.BytesIO(response.content), header=None)
        
        # 3. 截取前 13 列（根据 AAII 的标准格式）
        df = df.iloc[:, :13]
        
        # 4. 强制重命名列名，建立标准规范
        df.columns = [
            'Date', 'Bullish', 'Neutral', 'Bearish', 'Total',
            'Bullish_8w_Mov_Avg', 'Bull_Bear_Spread', 'Bullish_Average',
            'Bullish_Average_Plus_Std', 'Bullish_Average_Minus_Std',
            'SP500_Weekly_High', 'SP500_Weekly_Low', 'SP500_Weekly_Close'
        ]
        
        # ================= 数据清洗核心逻辑 =================
        
        # 核心 1：将 Date 列强转为日期。errors='coerce' 会把所有非日期的文本（表头、底部统计）变成 NaT
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # 核心 2：删除 Date 为 NaT 的行。这一步瞬间清除了上下两部分的所有杂乱数据！
        df = df.dropna(subset=['Date'])
        
        # 核心 3：清洗百分比数据（处理可能带 '%' 的字符串）
        def clean_pct(x):
            if pd.isna(x): return x
            if isinstance(x, str):
                x = x.replace('%', '').strip()
                try:
                    return float(x) / 100.0
                except ValueError:
                    return None
            return x

        pct_columns = [
            'Bullish', 'Neutral', 'Bearish', 'Total',
            'Bullish_8w_Mov_Avg', 'Bull_Bear_Spread', 'Bullish_Average',
            'Bullish_Average_Plus_Std', 'Bullish_Average_Minus_Std'
        ]
        for col in pct_columns:
            df[col] = df[col].apply(clean_pct)
            
        # 核心 4：清洗标普500指数数据（处理可能带千分位逗号的字符串，如 "6,903.46"）
        def clean_num(x):
            if pd.isna(x): return x
            if isinstance(x, str):
                x = x.replace(',', '').strip()
                try:
                    return float(x)
                except ValueError:
                    return None
            return x

        sp500_cols = ['SP500_Weekly_High', 'SP500_Weekly_Low', 'SP500_Weekly_Close']
        for col in sp500_cols:
            df[col] = df[col].apply(clean_num)
            
        # ==================================================
        
        # 5. 按日期排序并保存
        df = df.sort_values('Date')
        
        os.makedirs('data', exist_ok=True)
        file_path = 'data/aaii_sentiment.csv'
        # 保存时将日期格式化为 YYYY-MM-DD，去掉时分秒
        df.to_csv(file_path, index=False, date_format='%Y-%m-%d')
        
        print(f"✅ AAII 数据抓取并清洗成功！已保存至 {file_path}，共 {len(df)} 行。")

    except Exception as e:
        print(f"❌ AAII 抓取失败: {e}")

if __name__ == "__main__":
    fetch_aaii_sentiment()