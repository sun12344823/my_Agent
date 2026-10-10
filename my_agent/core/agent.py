"""Agent 抽象基类 —— 所有智能体的"祖先"（对标 Hello-Agents 7.3.3）

设计思想:
1. ABC + @abstractmethod: 强制所有子类必须实现 run(), 否则实例化直接报错
2. 共性收编: 名字/LLM/系统提示词/历史记录, 子类不用重复写
3. 子类只写差异: SimpleAgent 写对话循环, ReActAgent 写推理循环...
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from .config import Config
from .llm import MyLLM
from .message import Message


class Agent(ABC):
    """Agent 抽象基类

    子类必须实现 run() 方法 —— 这是"是个Agent就得能跑"的契约。
    第4课 SimpleAgent / 第5课 ReActAgent 都要继承这个类。
    """

    def __init__(
        self,
        name: str,
        llm: MyLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
    ):
        # 公共属性: 每个子类都会用到
        self.name = name                      # Agent 名字(如"旅行助手")
        self.llm = llm                        # 第1课造的 LLM 管家(传进来, 不是自己创建)
        self.system_prompt = system_prompt    # 系统提示词(Agent 的"人设")
        self.config = config or Config()      # 配置(不传就用默认)
        self._history: List[Message] = []     # 历史记录(注意下划线: 内部零件)

    # --------------------------------------------------
    # 抽象方法: 子类的"必答题"
    # --------------------------------------------------
    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """运行 Agent: 输入一句话, 返回回答

        每种 Agent 的核心差异就在这个方法里:
        - SimpleAgent: 调一次 LLM 就完事
        - ReActAgent: 思考→工具→观察 循环多次
        - 子类必须实现它, 否则实例化时报错(不是运行时才炸)
        """
        ...

    # --------------------------------------------------
    # TODO(你): 历史记录管理三件套
    # --------------------------------------------------
    def add_message(self, message: Message) -> None:
        """添加一条消息到历史记录

        步骤:
        1. 把 message 追加到 self._history 列表尾部
        2. 调用 self.trim_history() 防止历史无限膨胀
        """
        raise NotImplementedError("第2课 TODO: 请实现 add_message")

    def get_history(self) -> List[Message]:
        """获取历史记录副本(外部只读, 改了不影响内部)

        提示: return self._history.copy()
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """清空历史记录"""
        self._history.clear()

    def trim_history(self) -> None:
        """修剪历史: 超过 max_history_length 就删掉最旧的消息

        步骤:
        1. 读取 self.config.max_history_length (上限数字)
        2. 如果 len(self._history) > 上限:
           self._history = self._history[-上限:]   ← 切片, 保留最新N条
        """
        raise NotImplementedError("第2课 TODO: 请实现 trim_history")

    def __str__(self) -> str:
        return f"Agent(name={self.name})"
