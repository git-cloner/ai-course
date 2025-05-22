import gradio as gr
from typing import AsyncGenerator, List, Dict, Any
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession


async def chat_with_mcpserver(
        history: List[Dict[str, Any]]) -> AsyncGenerator[List[Dict[str, Any]], None]:
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.call_tool(
                "chat",
                {"messages": history}
            )
            text_content = response.content[0].text
            history.append({"role": "assistant", "content": text_content})
            yield history

css = """
#chatbot { min-height: 400px; }
.footer { 
    font-size: 0.8em; 
    margin-top: 10px; 
    text-align: center; 
    color: #666;
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# MCP Server Chat")

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        bubble_full_width=False,
        type="messages"
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="输入您的问题...",
            show_label=False,
            container=False,
            scale=7,
            autofocus=True
        )
        submit_btn = gr.Button("发送", variant="primary", scale=1)

    clear = gr.Button("清除对话记录", variant="secondary")

    async def user(user_message: str, history: List[Dict[str, Any]]) -> tuple[str, List[Dict[str, Any]]]:
        if not user_message.strip():
            return gr.skip(), history
        return "", history + [{"role": "user", "content": user_message}]

    submit_btn.click(
        user,
        [msg, chatbot],
        [msg, chatbot],
        queue=False
    ).then(
        chat_with_mcpserver, chatbot, chatbot
    )

    msg.submit(
        user,
        [msg, chatbot],
        [msg, chatbot],
        queue=False
    ).then(
        chat_with_mcpserver, chatbot, chatbot
    )

    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()
