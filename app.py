import streamlit as st
import cross_asset
import macro_economy
import market_internals
import sentiment_positioning
st.set_page_config(
    page_title="全球宏观与量化监控面板",
    page_icon="📈",
    layout="wide"
)

# 页面路由映射
PAGES = {
    "🌍 宏观经济与基本面": macro_economy,
    "🔀 跨市场与流动性": cross_asset,
    "📊 市场内部结构": market_internals,
    "🔥 情绪与仓位": sentiment_positioning
}

def main():
    # 侧边栏导航菜单
    st.sidebar.title("📈 全球宏观与量化监控面板")
    selection = st.sidebar.radio("选择页面", list(PAGES.keys()))
    
    # 动态加载页面
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()