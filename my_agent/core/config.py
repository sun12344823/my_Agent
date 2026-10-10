"""配置管理 —— 框架的"行为参数"集中地（对标 Hello-Agents 7.3.2）

设计思想:
1. 所有可调参数集中一处, 不散落在代码里(消灭魔法数字)
2. from_env() 支持环境变量覆盖 —— 复习第1课的 os.getenv!
"""

import os
from typing import Any, Dict, Optional

from pydantic import BaseModel


class Config(BaseModel):
    """框架全局配置

    用法:
        config = Config()                # 全默认值
        config = Config.from_env()       # 从环境变量读取(可覆盖)
        config = Config(temperature=0.3) # 手动指定
    """

    # --- LLM 配置 ---
    temperature: float = 0.7          # 采样温度: 越低越严谨, 越高越发散
    max_tokens: Optional[int] = None  # 单次回复最大长度(None=不限制)

    # --- 系统配置 ---
    debug: bool = False               # 调试模式: 打印更多中间过程
    log_level: str = "INFO"           # 日志级别

    # --- 对话配置 ---
    max_history_length: int = 100     # 历史记录最多保留几条

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量创建配置(没设的项用默认值)

        环境变量名: TEMPERATURE / MAX_TOKENS / DEBUG / LOG_LEVEL / MAX_HISTORY_LENGTH
        """
        return cls(
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None,
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_history_length=int(os.getenv("MAX_HISTORY_LENGTH", "100")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典(打印调试用)"""
        return self.model_dump()
