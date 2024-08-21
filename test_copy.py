import json
import time
import streamlit as st
from openai import OpenAI, RateLimitError

st.set_page_config(page_title="Math Helper")
st.title("Math Helper")


def chat(query, history):
    history.append({
        "role": "user",
        "content": query
    })
    client = OpenAI(
        api_key="sk-V5vPoqFdxtzmtPOqKf5OlRi2C8Vpzv4slZyQ9051ZiiOkxae",
        base_url="https://api.moonshot.cn/v1",
    )
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
        stream=True,
    )
    return response


def clear_chat_history():
    del st.session_state.messages


def init_chat_history():
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是Math Helper，很高兴为您服务🥰")

    if "messages" in st.session_state:
        for message in st.session_state.messages:
            avatar = '🧑‍💻' if message["role"] == "user" else '🤖'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    else:
        st.session_state.messages = []

    return st.session_state.messages


def main():
    history = init_chat_history()
    if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
        reset = False
        if reset:
            history = history[:-2]
            reset = False
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(prompt)
        collected_messages = ""
        # print(f"[user] {prompt}", flush=True)
        with st.chat_message("assistant", avatar='🤖'):
            placeholder = st.empty()
            try:
                response = chat(prompt, history)
            except RateLimitError as e:
                reset = True
                history.append({
                    "role": "assistant",
                    "content": "error"
                })
            if not reset:
                for chunk in response:
                    chunk_message = chunk.choices[0].delta
                    if not chunk_message.content:
                        continue
                    chunk_message = chunk_message.content
                    print(chunk_message)
                    collected_messages = collected_messages + chunk_message
                    placeholder.markdown(collected_messages)
                    time.sleep(0.01)
                    
            print(collected_messages)
            history.append({
                "role": "assistant",
                "content": collected_messages
            })
        print(json.dumps(history, ensure_ascii=False), flush=True)

        st.button("清空对话", on_click=clear_chat_history)


if __name__ == "__main__":
    main()
