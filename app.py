import streamlit as st

# ==========================================
# 1. 页面基础配置 (必须放在第一行)
# ==========================================
st.set_page_config(
    page_title="全天候宏观监控面板",
    page_icon="📈",
    layout="wide", # 使用宽屏模式，图表更大
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 左侧边栏导航设计
# ==========================================
st.sidebar.title("🧭 宏观交易监控台")
st.sidebar.markdown("---")

# 定义导航菜单
menu_options = {
    "宏观经济与基本面": "🏛️ 决定中长期趋势与美联储政策",
    "跨市场与流动性": "🌊 聪明钱的动向，极具前瞻性",
    "市场内部结构": "🔍 看透指数的虚假繁荣",
    "情绪与仓位": "🎭 寻找极值，反向操作"
}

# 使用 radio 组件作为导航
selected_page = st.sidebar.radio(
    "请选择监控模块：",
    list(menu_options.keys()),
    format_func=lambda x: f"{x}" # 这里可以自定义显示格式
)

# 在侧边栏底部显示当前模块的说明
st.sidebar.markdown("---")
st.sidebar.info(menu_options[selected_page])
st.sidebar.caption("最后更新时间: 实时/每日")

# ==========================================
# 3. 主页面内容渲染 (根据左侧选择切换)
# ==========================================

if selected_page == "宏观经济与基本面":
    st.title("🏛️ 宏观经济与基本面")
    st.markdown("#### 决定中长期趋势与美联储政策")
    
    # 使用 tabs (标签页) 让页面更整洁
    tab1, tab2, tab3 = st.tabs(["就业市场", "通胀数据", "经济景气度"])
    
    with tab1:
        st.subheader("初请失业金人数 (ICSA) & 非农就业")
        st.info("💡 提示：这里未来将接入 FRED API 的缓存数据。")
        # 占位符：st.line_chart(data)
        
    with tab2:
        st.subheader("核心 PCE & CPI 趋势")
        st.info("💡 提示：通胀拐点是美联储转向的核心指标。")
        
    with tab3:
        st.subheader("零售销售 & 纽约联储 WEI")

elif selected_page == "跨市场与流动性":
    st.title("🌊 跨市场与流动性")
    st.markdown("#### 聪明钱的动向，极具前瞻性")
    
    col1, col2 = st.columns(2) # 将页面分为左右两列
    
    with col1:
        st.subheader("美债收益率曲线 (10Y - 2Y)")
        st.warning("💡 提示：倒挂解除往往是衰退交易的开始。这里可接入 Yahoo Finance 数据。")
        
        st.subheader("VIX 恐慌指数")
        
    with col2:
        st.subheader("铜金比 (Copper/Gold Ratio)")
        st.success("💡 提示：这里可以直接嵌入 TradingView 的 HTML 组件，实现 0 延迟秒开！")
        # 示例：嵌入一个空的占位框代表 TradingView 图表
        st.components.v1.html(
            """<div style="background-color:#1E1E1E; height:300px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:white;">TradingView 铜金比图表占位</div>""", 
            height=310
        )
        
        st.subheader("油金比 (Oil/Gold Ratio)")

elif selected_page == "市场内部结构":
    st.title("🔍 市场内部结构")
    st.markdown("#### 看透指数的虚假繁荣")
    
    st.subheader("标普500成分股均线占比")
    st.markdown("观察是否有**“顶背离”**：指数创新高，但站上 50日/200日 均线的股票数量却在减少。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📈 高于 50 日均线占比 (MMFI)")
    with col2:
        st.info("📈 高于 200 日均线占比 (MMTH)")
        
    st.divider() # 分割线
    
    st.subheader("11大行业 ETF 相对强弱 (RSI/资金流向)")
    st.markdown("科技(XLK) vs 公用事业(XLU) vs 消费(XLY)")

elif selected_page == "情绪与仓位":
    st.title("🎭 情绪与仓位")
    st.markdown("#### 寻找极值，反向操作")
    
    st.markdown("> *当所有人都站在船的一侧时，船就要翻了。*")
    
    tab1, tab2, tab3 = st.tabs(["散户情绪", "机构仓位", "期权与投机"])
    
    with tab1:
        st.subheader("AAII 散户情绪指数 (每周四更新)")
        st.info("💡 提示：这里将读取 GitHub 仓库中爬虫定时更新的 CSV 文件。")
        st.metric(label="最新看多比例 (Bullish)", value="45.2%", delta="-2.1%") # 模拟数据展示
        
    with tab2:
        st.subheader("NAAIM 机构敞口指数 (每周三更新)")
        st.progress(75, text="当前机构仓位：75% (中等偏高)") # 使用进度条直观展示
        
    with tab3:
        st.subheader("COT 投机净仓位 & Put/Call Ratio")
        st.markdown("观察对冲基金在美股期货上的极端净多头或净空头。")