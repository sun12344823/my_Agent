"""统一 LLM 接口 —— my_agent 框架第一块基石

设计思想（对标 Hello-Agents 7.2）：
1. OpenAI 接口是行业事实标准，ModelScope/智谱/vLLM/Ollama 全兼容 → 只用一个 OpenAI 客户端
2. 多 provider 差异被压缩进一张 PROVIDER_PRESETS 预设表（差异的集合点）
3. provider 可以自动检测：框架根据环境变量推断用户在用哪家服务
4. 上层只调 invoke / stream_invoke，永远不需要知道背后是哪家模型
"""

import os
from typing import Any, Generator, Iterator, List, Optional

from openai import OpenAI

# ============================================================
# Provider 预设表：所有服务商差异集中于此
# 新增一家服务商 = 在这里加一个条目，其余代码零改动
# ============================================================
PROVIDER_PRESETS: dict = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1/",
        "model": "gpt-4o-mini",
    },
    "modelscope": {
        "api_key_env": "MODELSCOPE_API_KEY",
        "base_url": "https://api-inference.modelscope.cn/v1/",
        "model": "Qwen/Qwen2.5-72B-Instruct",
    },
    "zhipu": {
        "api_key_env": "ZHIPU_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "model": "glm-4-flash",
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "ollama": {
        "api_key_env": "OLLAMA_API_KEY",  # 本地服务通常无需真实 key
        "base_url": "http://localhost:11434/v1",
        "model": "qwen2.5:3b",
    },
}

# 通用环境变量（.env.example 里的 LLM_* 四件套）
UNIFIED_MODEL_ENV = "LLM_MODEL_ID"
UNIFIED_API_KEY_ENV = "LLM_API_KEY"
UNIFIED_BASE_URL_ENV = "LLM_BASE_URL"
UNIFIED_TIMEOUT_ENV = "LLM_TIMEOUT"

DETECT_RULES = [
        ("MODELSCOPE_API_KEY", "modelscope"),
        ("ZHIPU_API_KEY", "zhipu"),
        ("DEEPSEEK_API_KEY", "deepseek"),
        ("OPENAI_API_KEY", "openai"),
    ]


class MyLLM:
    """统一 LLM 客户端

    用法:
        llm = MyLLM()                    # 自动检测 provider
        llm = MyLLM(provider="modelscope")  # 手动指定
        text = llm.invoke([{"role": "user", "content": "你好"}])
    """

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        timeout: float = 60.0,
    ):
        # 1. 自动检测 provider（未显式指定时）
        self.provider = provider or self._detect_provider()
        if self.provider not in PROVIDER_PRESETS:
            supported = ", ".join(sorted(PROVIDER_PRESETS))
            raise ValueError(
                f"不支持的 provider '{self.provider}'，支持的有: {supported}"
            )

        # 2. 查预设表 + 环境变量解析凭证
        preset = PROVIDER_PRESETS[self.provider]
        self.api_key = (
            api_key
            or os.getenv(UNIFIED_API_KEY_ENV)
            or os.getenv(preset["api_key_env"])
        )
        self.base_url = (
            base_url
            or os.getenv(UNIFIED_BASE_URL_ENV)
            or preset["base_url"]
        )
        self.model = (
            model
            or os.getenv(UNIFIED_MODEL_ENV)
            or preset["model"]
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                f"provider '{self.provider}' 需要提供 api_key："
                f"请在 .env 中设置 {UNIFIED_API_KEY_ENV} 或 {preset['api_key_env']}"
            )
        if not self.base_url:
            raise ValueError(f"provider '{self.provider}' 缺少 base_url")

        # 3. 创建 OpenAI 兼容客户端（框架唯一的网络依赖点）
        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    # --------------------------------------------------
    # TODO(你): 实现自动检测逻辑
    # --------------------------------------------------
   

    def _detect_provider(self) -> str:
        """根据环境变量推断当前使用的 LLM 服务商

        规则（优先级从高到低）：
        1. 设置了 MODELSCOPE_API_KEY → "modelscope"
        2. 设置了 ZHIPU_API_KEY     → "zhipu"
        3. 设置了 DEEPSEEK_API_KEY  → "deepseek"
        4. 设置了 OPENAI_API_KEY    → "openai"
        5. 以上都没有，但设置了 LLM_BASE_URL 且包含 "11434"（Ollama 默认端口）→ "ollama"
        6. 兜底返回 "openai"

        提示: os.getenv(name) 返回 None 或字符串，空字符串视为未设置。
        """
        for env_name, provider_name in DETECT_RULES:
            if os.getenv(env_name):
                return provider_name

        base_url = os.getenv("LLM_BASE_URL") or ""
        if "11434" in base_url:
            return "ollama"
        return "openai"


    # --------------------------------------------------
    # TODO(你): 实现统一调用入口
    # --------------------------------------------------
    def invoke(self, messages: List[dict], **kwargs) -> str:
        """非流式调用：发送消息，返回完整回复文本

        步骤：
        1. 组装请求参数: model / messages / temperature，max_tokens 不为 None 时才传
        2. 调用 self._client.chat.completions.create(**请求参数, **kwargs)
        3. 从响应中取出第一条 choice 的 message.content 并返回

        提示: content 可能为 None（极端情况），此时返回空字符串。
        """
        raise NotImplementedError("第1课 TODO 2: 请实现 invoke")

    # --------------------------------------------------
    # 流式调用：我直接给你（观察 yield 用法，第 4 课 SimpleAgent 会用到）
    # --------------------------------------------------
    def stream_invoke(self, messages: List[dict], **kwargs) -> Iterator[str]:
        """流式调用：逐块 yield 回复文本片段"""
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
        }
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        params.update(kwargs)

        stream = self._client.chat.completions.create(**params)
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def __repr__(self) -> str:
        return (
            f"MyLLM(provider={self.provider}, model={self.model}, "
            f"base_url={self.base_url})"
        )
