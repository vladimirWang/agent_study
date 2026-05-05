import time
import streamlit as st
from rag import RagService

st.title("智能客服")

st.divider()

if 'message' not in st.session_state:
    st.session_state['message'] = [
        {"role": "assistant", "content": "你好，我是某东客服，有什么可以帮你的吗？"}
    ]

messages = st.session_state['message']
for message in messages:
    st.chat_message(message['role']).write(message['content'])
    # with st.chat_message(message['role']):
    #     st.write(message['content'])

prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)

    st.session_state['message'].append({"role": "user", "content": prompt})

    with st.spinner("思考中..."):
        time.sleep(1)
        st.chat_message("assistant").write('fasdf')
        st.session_state['message'].append({"role": "assistant", "content": 'fasdf'})

# st.session_state.setdefault("session_id", "user001")

# rag_service = RagService()

# user_input = st.text_input("请输入你的问题")

# if st.button("提交"):
#     res = rag_service.chain.invoke({"input": user_input}, session_config)
#     st.write(res)