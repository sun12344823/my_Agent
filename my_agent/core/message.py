"""消息系统 —— 框架的"话语"统一格式（对标 Hello-Agents 7.3.1）

设计思想:
1. pydantic BaseModel 穿"紧身衣": role 只许四种, content 只许字符串
2. 对内丰富(timestamp/metadata), 对外兼容(to_dict 直接给 OpenAI API 用)
"""

from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field

# 角色类型: 只允许这四种取值(和 OpenAI API 规范一一对应)
MessageRole = Literal["user", "assistant", "system", "tool"]


class Message(BaseModel):
    """一条对话消息

    用法:
        msg = Message(content="你好", role="user")
        print(msg)                          # [user] 你好
        api_format = msg.to_dict()          # {"role": "user", "content": "你好"}
    """

    content: str                                # 消息内容(只许字符串)
    role: MessageRole                           # 谁说的(只许四种角色)
    timestamp: Optional[datetime] = None        # 什么时候说的(自动填)
    metadata: Optional[Dict[str, Any]] = None   # 扩展槽位(暂不用, 预留)

    def model_post_init(self, __context) -> None:
        """pydantic 钩子: 字段验证通过后自动补默认值"""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """转换为 OpenAI API 格式(对外兼容的关键)"""
        return {"role": self.role, "content": self.content}

    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"
