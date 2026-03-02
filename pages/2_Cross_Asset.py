import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 页面配置
st.set_page_config(page_title="跨市场与流动性", page_icon="🔀", layout="wide")

st.title("🔀 跨市场与流动性 (Cross Asset & Liquidity)")
st.markdown("---")
st.markdown("通过跨资产比价与宏观利率指标，监控全球资金流向与宏观流动性拐点。")

# 通用数据加载函数
@st.cache_data
def load_data(file_name):
    try:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(root_dir, 'data', file_name)
        if not os.path.exists(file_path):
            return pd.DataFrame()
        return pd.read_csv(file_path, index_col=0, parse_dates=True)
    except Exception as e:
        st.error(f"加载数据失败 {file_name}: {e}")
        return pd.DataFrame()

# 加载所有需要的数据
df_cross = load_data('oil_gold_ copper.csv')
df_inflation = load_data('fred_inflation.csv')
df_financial = load_data('fred_financial.csv')

# 创建 5 个选项卡
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🥉 铜金比 vs PPI", 
    "🛢️ 油金比 vs CPI", 
    "📈 10年期美债 vs 利率", 
    "📉 收益率曲线(10Y-2Y)", 
    "⚠️ CCC信用利差"
])

def create_dual_axis_chart(df1, col1, name1, df2, col2, name2, title, 
                          color1='#b87333', color2='#1f77b4', 
                          height=600):
    
    # 1. 确定完整的日期范围
    # 取两个数据集中最早的开始时间和最晚的结束时间
    if df1.empty or df2.empty:
        st.warning("数据不足，无法绘图")
        return go.Figure()

    start_date = max(df1.index.min(), df2.index.min())
    end_date = min(df1.index.max(), df2.index.max())
    
    # 生成完整的日历日索引
    full_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 2. 重采样并填充数据 (Forward Fill)
    # 先重索引到完整日期，然后向前填充，处理缺失值
    d1 = df1.reindex(full_index).ffill()
    d2 = df2.reindex(full_index).ffill()
    
    y1_data = d1[col1]
    y2_data = d2[col2]
    
    y1_title = name1
    y2_title = name2

    # 创建双轴图表
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 添加轨迹
    fig.add_trace(
        go.Scatter(x=full_index, y=y1_data, name=name1, line=dict(color=color1, width=2), connectgaps=True),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=full_index, y=y2_data, name=name2, line=dict(color=color2, width=2), connectgaps=True),
        secondary_y=True
    )
    
    # 布局设置
    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=height,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_yaxes(title_text=y1_title, title_font=dict(color=color1), tickfont=dict(color=color1), secondary_y=False)
    fig.update_yaxes(title_text=y2_title, title_font=dict(color=color2), tickfont=dict(color=color2), secondary_y=True)

    return fig

with tab1:
    st.subheader("铜金比 vs PPI (Copper/Gold Ratio vs PPI)")
    st.markdown("""
    * **核心逻辑**：铜金比反映全球总需求，PPI 反映工业品价格。两者通常高度正相关。
    * **背离信号**：如果铜金比下跌而 PPI 还在上涨，预示 PPI 即将见顶回落（通胀降温/通缩风险）。
    """)
    
    if not df_cross.empty and not df_inflation.empty:
        # 确保列名存在
        if 'Copper_Gold_Ratio' in df_cross.columns and 'PPI(PPIACO)' in df_inflation.columns:
            fig1 = create_dual_axis_chart(
                df_cross, 'Copper_Gold_Ratio', '铜金比',
                df_inflation, 'PPI(PPIACO)', 'PPI (全部商品)',
                title="铜金比 vs PPI",
                color1='#b87333', # 铜色
                color2='#00cc96'  # 绿色
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("数据列缺失，请检查数据文件。")
    else:
        st.warning("暂无数据，请运行相关脚本获取数据。")

with tab2:
    st.subheader("油金比 vs CPI (Oil/Gold Ratio vs CPI)")
    st.markdown("""
    * **核心逻辑**：原油价格直接影响通胀预期。油金比领先或同步于 CPI。
    * **预警信号**：油金比大幅下挫通常预示 CPI 将随之下行（通缩压力）。
    """)
    
    if not df_cross.empty and not df_inflation.empty:
         if 'Oil_Gold_Ratio' in df_cross.columns and 'CPI(CPIAUCSL)' in df_inflation.columns:
            fig2 = create_dual_axis_chart(
                df_cross, 'Oil_Gold_Ratio', '油金比',
                df_inflation, 'CPI(CPIAUCSL)', 'CPI (消费者价格指数)',
                title="油金比 vs CPI",
                color1='orange', 
                color2='#AB63FA' 
            )
            st.plotly_chart(fig2, use_container_width=True)
         else:
            st.warning("数据列缺失，请检查数据文件。")
    else:
        st.warning("暂无数据，请运行相关脚本获取数据。")

with tab3:
    st.subheader("10年期国债收益率 vs 联邦基金利率")
    st.markdown("""
    * **指标属性**：同步/滞后
    * **核心逻辑**：**资金成本**。10年期美债收益率是市场无风险利率的基准，通常受美联储加息/降息预期（联邦基金利率）的牵引。
    * **观察重点**：当10年期美债收益率大幅高于联邦基金利率时，市场预期加息；反之则预期降息。
    """)
    
    if not df_financial.empty:
         # 检查列名是否存在
         cols = df_financial.columns
         rate_col = '联邦基金利率(FEDFUNDS)'
         yield_col = '10年期美债收益率(DGS10)'
         
         if rate_col in cols and yield_col in cols:
            fig3 = create_dual_axis_chart(
                df_financial, rate_col, '联邦基金利率',
                df_financial, yield_col, '10年期美债收益率',
                title="10年期美债收益率 vs 联邦基金利率",
                color1='#EF553B', # 红色
                color2='#636EFA'  # 蓝色
            )
            # 对于利率对比，通常放在同一个轴上更直观，这里强制双轴但刻度范围接近时也易于观察
            # 或者我们可以自定义 update_yaxes 让它们共享一个轴，但 create_dual_axis_chart 默认是双轴。
            # 鉴于两者量级相同（都是百分比），双轴也无妨，或者稍后优化为单轴多线。
            st.plotly_chart(fig3, use_container_width=True)
         else:
            st.warning(f"数据列缺失。可用列: {cols.tolist()}")
    else:
        st.warning("暂无数据，请运行 fetch_fred.py 脚本获取数据。")

with tab4:
    st.subheader("收益率曲线 10Y-2Y (Yield Curve Inversion)")
    st.markdown("""
    * **指标属性**：绝对领先
    * **核心逻辑**：**主跌浪开启**。倒挂本身不跌，解除倒挂的那一刻才是暴跌的开始（因为短期利率因恐慌性降息而暴跌）。
    * **预警信号**：从倒挂 ($<0$) 急速回升至 $>0$。
    """)
    # 10年期收益率 - 2年期收益率

with tab5:
    st.subheader("CCC 级信用利差 (CCC High Yield Credit Spread)")
    st.markdown("""
    * **指标属性**：领先/同步
    * **核心逻辑**：**流动性危机**。债券市场的“恐慌指数”。利差飙升说明底层企业借不到钱，股市极大概率发生股灾。
    * **预警信号**：利差突然飙升突破 $10\%$。
    """)
    # TradingView 直接调用 FRED 数据库的 CCC 级期权调整利差