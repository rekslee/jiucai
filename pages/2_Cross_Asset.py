import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
# 页面配置
st.set_page_config(page_title="跨市场与流动性", page_icon="🔀", layout="wide")

st.title("🔀 跨市场与流动性 (Cross Asset & Liquidity)")
st.markdown("---")
st.markdown("通过跨资产比价与宏观利率指标，监控全球资金流向与宏观流动性拐点。")

# 定义一个函数，用于动态生成 TradingView 的嵌入代码
def render_tradingview_widget(symbol, height=500):
    # 清理 symbol 中的特殊字符，用于生成合法的 HTML ID
    clean_id = symbol.replace(':', '_').replace('/', '_').replace('!', '_').replace('-', '_')
    
    html_code = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container" style="height:{height}px;width:100%">
      <div id="tradingview_{clean_id}" style="height:calc(100% - 32px);width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "D",
      "timezone": "Asia/Shanghai",
      "theme": "dark",
      "style": "1",
      "locale": "zh_CN",
      "enable_publishing": false,
      "backgroundColor": "#131722",
      "gridColor": "rgba(42, 46, 57, 0.06)",
      "hide_top_toolbar": false,
      "hide_legend": false,
      "save_image": false,
      "container_id": "tradingview_{clean_id}"
    }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    # 使用 Streamlit 的 components 渲染 HTML
    components.html(html_code, height=height)

# 创建 5 个选项卡
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🥉 铜金比", 
    "🛢️ 油金比", 
    "📈 10年期美债", 
    "📉 收益率曲线(10Y-2Y)", 
    "⚠️ CCC信用利差"
])

with tab1:
    st.subheader("铜金比 (Copper/Gold Ratio)")
    st.markdown("""
    * **指标属性**：绝对领先
    * **核心逻辑**：**顶背离**。铜代表工业需求，金代表避险。比值下降说明聪明钱在买黄金避险，股市极大概率即将补跌。
    * **预警信号**：股市创新高，但铜金比持续暴跌。
    """)
    # TradingView 支持直接输入公式：COMEX铜 / COMEX黄金
    render_tradingview_widget("COMEX:HG1!/COMEX:GC1!")
    st.title("美股宏观先行指标：油金比")

    # 1. 获取数据 (CL=F 是原油期货, GC=F 是黄金期货)
    @st.cache_data
    def get_oil_gold_ratio():
        oil = yf.download("CL=F", period="2y")['Close']
        gold = yf.download("GC=F", period="2y")['Close']
        
        # 对齐日期并计算比率
        df = pd.concat([oil, gold], axis=1)
        df.columns = ['Oil', 'Gold']
        df['Ratio'] = df['Oil'] / df['Gold']
        return df.dropna()

    data = get_oil_gold_ratio()

    # 2. 绘图 (使用 Plotly 达到类似 TradingView 的交互效果)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Ratio'], name="油金比", line=dict(color='orange')))

    fig.update_layout(
        title="油金比 (Oil/Gold Ratio) 历史走势",
        xaxis_title="日期",
        yaxis_title="比率",
        template="plotly_dark" # 使用暗色模式，更有科技感
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("油金比 (Oil/Gold Ratio)")
    st.markdown("""
    * **指标属性**：领先
    * **核心逻辑**：**通缩风险**。原油是工业的血液，油价跌金价涨，说明市场对全球经济极度悲观。
    * **预警信号**：油金比大幅下挫。
    """)
    # NYMEX原油 / COMEX黄金
    render_tradingview_widget("NYMEX:CL1!/COMEX:GC1!")

with tab3:
    st.subheader("10年期国债收益率 (US 10Y Treasury Yield)")
    st.markdown("""
    * **指标属性**：同步
    * **核心逻辑**：**杀估值**。10年期美债是所有资产的“地心引力”。无风险收益太高，资金从股市抽离，科技股重挫。
    * **预警信号**：收益率急速飙升（如突破 $4.5\%$）。
    """)
    # 10年期美债收益率
    render_tradingview_widget("TVC:US10Y")

with tab4:
    st.subheader("收益率曲线 10Y-2Y (Yield Curve Inversion)")
    st.markdown("""
    * **指标属性**：绝对领先
    * **核心逻辑**：**主跌浪开启**。倒挂本身不跌，解除倒挂的那一刻才是暴跌的开始（因为短期利率因恐慌性降息而暴跌）。
    * **预警信号**：从倒挂 ($<0$) 急速回升至 $>0$。
    """)
    # 10年期收益率 - 2年期收益率
    render_tradingview_widget("TVC:US10Y-TVC:US02Y")

with tab5:
    st.subheader("CCC 级信用利差 (CCC High Yield Credit Spread)")
    st.markdown("""
    * **指标属性**：领先/同步
    * **核心逻辑**：**流动性危机**。债券市场的“恐慌指数”。利差飙升说明底层企业借不到钱，股市极大概率发生股灾。
    * **预警信号**：利差突然飙升突破 $10\%$。
    """)
    # TradingView 直接调用 FRED 数据库的 CCC 级期权调整利差
    render_tradingview_widget("FRED:BAMLH0A3CRPIEY")