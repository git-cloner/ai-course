from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY"
)
model_name = "deepseek"

# 初始化聊天记录
if 'messages' not in st.session_state:
    st.session_state.messages = []

def clear_chat_history():
    st.session_state.messages = []

def init_sidebar():
    st.sidebar.title('AI Chatbot')
    # 温度
    temperature = st.sidebar.slider(
        '温度', min_value=0.01, max_value=1.0, value=0.9, step=0.1, key='temperature')
    # top_p
    top_p = st.sidebar.slider('累计概率采样', min_value=0.01,
                              max_value=1.0, value=0.9, step=0.1, key='top_p')
    # 最大长度
    max_length = st.sidebar.slider(
        '最大长度', min_value=64, max_value=4096, value=512, step=8, key='max_length')
    # 清除聊天历史
    st.sidebar.button('清除会话记录', on_click=clear_chat_history)

def chat_bot():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input(placeholder="请输入您的问题", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        model = st.session_state.get('selected_model', model_name)
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p,
                    max_tokens=st.session_state.max_length,
                )
                response = ""
                placeholder = st.empty()
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        response += chunk.choices[0].delta.content
                        placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    init_sidebar()
    chat_bot()