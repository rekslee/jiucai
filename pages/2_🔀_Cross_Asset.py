import streamlit as st
import pandas as pd
import numpy as np

def app():
    st.title("📊 数据分析页面")
    
    # 生成示例数据
    data = pd.DataFrame(
        np.random.randn(50, 3),
        columns=['A列', 'B列', 'C列']
    )
    
    st.write("""
    ### 随机数据展示
    这是一个简单的数据可视化示例
    """)
    
    # 图表展示
    st.line_chart(data)
    st.bar_chart(data)
    
    # 条件显示原始数据
    if st.checkbox("显示原始数据"):
        st.dataframe(data)