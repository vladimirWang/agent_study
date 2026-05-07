import time
import streamlit as st
from rag import RagService
import config_data as config

st.title("智能客服")

st.divider()

if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService()

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

    ai_res_list = []
    with st.spinner("思考中..."):
        # time.sleep(1)
        res = st.session_state['rag'].chain.stream({"input": prompt}, config.session_config)
        def capture_stream(generator, cache_list):
            for chunk in generator:
                # st.chat_message("assistant").write(chunk.content)
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture_stream(res, ai_res_list))
        st.session_state['message'].append({"role": "assistant", "content": "".join(ai_res_list)})
        # 

# st.session_state.setdefault("session_id", "user001")

# rag_service = RagService()

# user_input = st.text_input("请输入你的问题")

# if st.button("提交"):
#     res = rag_service.chain.invoke({"input": user_input}, session_config)
#     st.write(res)