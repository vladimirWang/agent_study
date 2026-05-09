from typing import Callable
from utils.prompt_loader import load_report_prompts, load_system_prompts
from langchain.agents import AgentState
from langchain.agents.middleware import Runtime, dynamic_prompt, wrap_tool_call, before_model
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.logger_handler import logger
from langchain.agents.middleware import ModelRequest


# 工具执行的监控
@wrap_tool_call
def monitor_tool(request: ToolCallRequest, handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command: 
    # 请求的数据封装，执行的函数本身
    logger.info(f"[tool monitor]执行工具: {request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数: {request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[tool monitor]调用成功: {request.tool_call['name']}, 处理结果: {result}")
        if request.tool_call['name'] == 'fill_context_for_report':
            request.runtime.context['report'] = True

        return result
    except Exception as e:
        logger.error(f"[tool monitor]调用失败: {request.tool_call['name']}, 失败原因: {str(e)}")
        raise e

# 模型执行前输出日志
@before_model
def log_before_model(state: AgentState, runtime: Runtime): 
    logger.info(f"[log_before_model]即将调用模型： 带有{len(state['messages'])}条消息")
    last_msg = state['messages'][-1]
    logger.debug(f"[log_before_model] 消息类型: {type(last_msg).__name__}, 消息内容 {last_msg.content.strip()}")
    return None

@dynamic_prompt # 每一次在生成提示词前调用此函数
def report_prompt_switch(request: ModelRequest): # 动态切换提示词
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()
    return load_system_prompts()