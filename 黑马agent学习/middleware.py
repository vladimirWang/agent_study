from langchain.agents import AgentState, create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.tools import tool
from dotenv import load_dotenv
from langgraph.runtime import Runtime
from langchain.agents.middleware import after_model, before_agent, after_agent, before_model, wrap_model_call, wrap_tool_call

load_dotenv()

model = ChatTongyi(
    model="qwen3-max"
)
@tool(description="获取天气信息, 传入城市名称字符串， 返回天气字符串")
def get_weather(city: str)-> str:
    return f"{city}晴天"

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime)-> None:
    print(f"[before agent] agent启动, 并附带{len(state["messages"])}条消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime)-> None:
    print(f"[after agent] agent结束, 并附带{len(state["messages"])}条消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime)-> None:
    print(f"[before model] model即将调用, 并附带{len(state["messages"])}条消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime)-> None:
    print(f"[after model] 模型调用结束, 并附带{len(state["messages"])}条消息")


@wrap_model_call
def model_call_hook(request, handler):
    print(f"[model_call_hook] 模型调用了")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"[tool_call_hook] 工具执行 name: {request.tool_call["name"]}")
    print(f"[tool_call_hook] 工具执行 参数: {request.tool_call["args"]}")
    return handler(request)

agent = create_agent(
    model=model,
    tools=[get_weather],
    # system_prompt="你是一个智能助理"
    middleware=[
        log_before_agent, log_after_agent, log_before_model, 
        log_after_model, model_call_hook, tool_call_hook
    ]
)

res = agent.invoke({
    "messages": [
        {"role": "user", "content": "今天上海天气怎么样"}
    ],
}, stream_mode="values")

print(type(res), res)

# for chunk in stream:
#     last_msg = chunk["messages"][-1]
#     if last_msg.content:
#         print(f"agent: {last_msg.content}")
#     else:
#         print(f"calling too: {[tc["name"] for tc in last_msg.tool_calls]}")