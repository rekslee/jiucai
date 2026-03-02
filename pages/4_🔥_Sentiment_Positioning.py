import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="情绪与仓位", page_icon="🔥", layout="wide")

st.title("🔥 情绪与仓位 (Sentiment & Positioning)")
st.markdown("---")

st.markdown("本页面监控市场参与者的情绪极值与真实资金仓位，用于寻找**反向交易（Contrarian）**的机会。")

tab1, tab2, tab3 = st.tabs(["散户情绪 (AAII)", "机构仓位 (NAAIM)", "投机净头寸 (CFTC)"])

with tab1:
    st.subheader("AAII 散户情绪指数")
    st.info("🚧 图表开发中... 将读取 data/aaii_sentiment.csv")

with tab2:
    st.subheader("NAAIM 机构主动仓位")
    st.info("🚧 图表开发中... 将读取 data/naaim_exposure.csv")

with tab3:
    st.subheader("CFTC COT 核心资产净投机仓位")
    st.info("🚧 图表开发中... 将读取 data/cftc_cot.csv")