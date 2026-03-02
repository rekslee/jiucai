import streamlit as st

def app():
    st.title("欢迎来到主页")
    st.write("""
    ## 这是一个Streamlit多页面应用示例
    使用左侧导航栏切换不同页面
    """)
    
    # 图片展示
    st.image("https://picsum.photos/800/400?random=1", 
             caption="示例图片", 
             use_column_width=True)
    
    # 两列布局
    col1, col2 = st.columns(2)
    with col1:
        st.success("左侧内容区域")
        st.write("这里可以放置一些介绍性内容")
    
    with col2:
        st.info("右侧内容区域")
        st.write("这里可以放置其他补充信息")