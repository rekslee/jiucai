import streamlit as st

st.set_page_config(
    page_title="全球宏观与量化监控面板",
    page_icon="📈",
    layout="wide"
)

st.title("📈 全球宏观与量化监控面板")
st.markdown("---")

st.markdown("""
### 欢迎使用！

* **🌍 Macro Economy (宏观经济与基本面)**
  * 经济增长、通胀、就业、制造业 PMI 等核心宏观指标。
* **🔀 Cross Asset (跨市场与流动性)**
  * 股债汇大宗商品比价、美联储资产负债表、金融条件指数。
* **📊 Market Internals (市场内部结构)**
  * 市场宽度、领涨板块、新高新低比例、上涨/下跌家数。
* **🔥 Sentiment & Positioning (情绪与仓位)**
  * 散户情绪 (AAII)、机构仓位 (NAAIM)、投机净头寸 (CFTC COT) 等。
""")

st.info("👈 请点击左侧菜单开始探索。")