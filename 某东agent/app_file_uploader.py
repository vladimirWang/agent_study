import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

st.title("知识库更新服务")

file = st.file_uploader("请上传文件", type=["txt"], accept_multiple_files=False)

if "service" not in st.session_state:
    st.session_state['service'] = KnowledgeBaseService()

if file != None:
    file_name = file.name
    file_type = file.type
    file_size = file.size/1024
    st.subheader(f"文件名: {file_name}")
    st.write(f"文件格式: {file_type} | 文件大小: {file_size:.2f}kb")

    text = file.getvalue().decode("utf-8")
    # st.write(text)
    service = st.session_state['service']
    
    with st.spinner("载入中..."):
        time.sleep(1)
        result = service.upload_by_str(text, file_name)
        st.write(result)
