from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from utils.config_handler import prompts_conf

def load_system_prompts():
    keyname = 'main_prompt_path'
    try:
        system_prompt_path = get_abs_path(prompts_conf[keyname])
    except KeyError as e:
        logger.error(f"[load_system_prompts] 配置文件中没有找到 {keyname}配置项")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts] 解析系统提示词失败: {str(e)}")
        raise e

def load_rag_prompts():
    keyname = 'rag_summarize_prompt_path'
    try:
        rag_prompt_path = get_abs_path(prompts_conf[keyname])
    except KeyError as e:
        logger.error(f"[load_rag_prompts] 配置文件中没有找到 {keyname}配置项")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts] 解析系统提示词失败: {str(e)}")
        raise e

def load_report_prompts():
    keyname = 'report_prompt_path'
    try:
        report_prompt_path = get_abs_path(prompts_conf[keyname])
    except KeyError as e:
        logger.error(f"[load_report_prompts] 配置文件中没有找到 {keyname}配置项")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts] 解析系统提示词失败: {str(e)}")
        raise e


if __name__ == "__main__":
    # print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())