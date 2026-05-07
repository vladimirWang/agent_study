from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.tools import tool
from dotenv import load_dotenv

load_dotenv()

model = ChatTongyi(
    model="qwen3-max"
)
@tool(description="获取天气信息")
def get_weather()-> str:
    return "晴天"

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个智能助理"
)

stream = agent.stream({
    "messages": [
        {"role": "user", "content": "今天上海天气怎么样"}
    ]
}, stream_mode="values")

print(type(stream), stream)

for chunk in stream:
    last_msg = chunk["messages"][-1]
    if last_msg.content:
        print(f"agent: {last_msg.content}")
    else:
        print(f"calling too: {[tc["name"] for tc in last_msg.tool_calls]}")