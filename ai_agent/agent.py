# ai_agent/agent.py
import os
from typing import List
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 加载 .env 文件
load_dotenv()

class AIAgent:
    def __init__(self):
        api_key = os.getenv("ALIYUN_DASHSCOPE_API_KEY")
        if not api_key:
            raise EnvironmentError("未设置 ALIYUN_DASHSCOPE_API_KEY，请在 .env 文件中配置")
        dashscope.api_key = api_key

    def generate_shell_commands(self, user_input: str) -> List[str]:
        """将自然语言转换为 Shell 命令列表（允许包含危险命令）"""
        prompt = f"""你是一个 Linux 终端助手。请将以下用户请求转换为精确、高效的 Bash 命令。
要求：
- 返回纯命令列表，每行一条命令
- 不要包含解释、注释或 markdown
- 优先使用安全命令；仅在绝对必要时才使用高危命令（如 rm、dd、mkfs）
- 确保命令可直接在 bash 中执行

用户请求: {user_input}
命令:"""

        try:
            response = Generation.call(
                model="qwen-max",
                prompt=prompt,
                result_format="text"
            )
            text = response.output.text.strip()
            if not text:
                return []
            # 按行分割，过滤空行
            commands = [line.strip() for line in text.split('\n') if line.strip()]
            return commands
        except Exception as e:
            raise RuntimeError(f"AI 生成失败: {e}")
