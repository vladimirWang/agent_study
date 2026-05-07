from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.tools import tool
from dotenv import load_dotenv

load_dotenv()

model = ChatTongyi(
    model="qwen3-max"
)
@tool(description="查询股价")
def get_price(name: str)-> str:
    return f"股票{name}价格是20元"

@tool(description="查询公司信息")
def get_info(name: str)-> str:
    return f"股票{name}是一家a股上市公司"

agent = create_agent(
    model=model,
    tools=[get_price, get_info],
    system_prompt="你是一个智能助理， 可以回答股票相关问题，请告诉我思考过程，让我知道你为什么调用某个工具"
)

stream = agent.stream({
    "messages": [
        {"role": "user", "content": "传智教育股价多少，介绍一下"}
    ]
}, stream_mode="values")

# print(type(stream), stream)

for chunk in stream:
    last_msg = chunk["messages"][-1]
    if last_msg.content:
        print(f"agent: {last_msg.content}")
    try:
        if last_msg.tool_calls:
            print(f"calling too: {[tc["name"] for tc in last_msg.tool_calls]}")
    except AttributeError as e:
        pass