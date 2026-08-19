import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot")
st.caption("🚀 基于火山方舟 · DeepSeek 的聊天机器人")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好！我是人工智能助手，有什么可以帮你？"}
    ]

# ✅ 从 Streamlit Secrets 读密钥，绝不写死在代码里
api_key = st.secrets.get("ARK_API_KEY", "")

with st.sidebar:
    st.header("⚙️ 设置")
    if api_key:
        st.success("已读取 API Key（来自 Secrets）")
    else:
        st.warning("未配置 ARK_API_KEY，请在 Streamlit Secrets 中设置")
    model = st.selectbox(
        "模型",
        ["deepseek-v4-flash-ga-260731"],  # 你在方舟里实际可用的模型 ID
    )
    st.markdown("[去火山方舟获取 API Key](https://console.volcengine.com/ark)")

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("说点什么..."):
    if not api_key:
        st.info("请先在 Streamlit Secrets 中配置 ARK_API_KEY。", icon="🔑")
        st.stop()

    # ✅ base_url 指向火山方舟的 OpenAI 兼容地址
    client = OpenAI(
        api_key=api_key,
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "你是人工智能助手."}]
                 + st.session_state["messages"],
        stream=True,
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                placeholder.write(full_response)
    st.session_state["messages"].append({"role": "assistant", "content": full_response})
