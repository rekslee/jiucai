import streamlit as st

def app():
    st.title("⚙️ 设置页面")
    
    # 用户设置区域
    with st.expander("用户设置"):
        username = st.text_input("用户名")
        dark_mode = st.checkbox("启用暗黑模式")
        font_size = st.slider("字体大小", 12, 24, 16)
    
    # 系统信息区域
    with st.expander("系统信息"):
        st.write(f"Streamlit版本: {st.__version__}")
        st.write("这是一个演示应用")
    
    # 保存按钮
    if st.button("保存设置"):
        st.success("设置已保存!")
        st.balloons()