from fastmcp import FastMCP
import asyncio
from openai import OpenAI

mcp = FastMCP("DeepSeek-Chatbot", transport="sse")


@mcp.tool()
def chat(messages) -> str:
    client = OpenAI(
        base_url="https://gitclone.com/qchain/v1", api_key="EMPTY")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )
    full_text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            full_text = full_text + chunk.choices[0].delta.content
    return full_text


if __name__ == "__main__":
    mcp.run(transport='sse', port=8000)
