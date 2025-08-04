"""LLM client and factory utilities."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class LLMClient:
    """Client for invoking large language models."""

    provider: str
    model: str
    temperature: float
    timeout: float
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    max_tokens: int = 1024

    @classmethod
    def from_config(
        cls,
        config_path: str = "config/llm.yaml",
        *,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[float] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> "LLMClient":
        """Instantiate an :class:`LLMClient` from configuration.

        Parameters override values from the YAML file. Each value may also be
        supplied via environment variables:

        - ``LLM_PROVIDER``
        - ``LLM_MODEL``
        - ``LLM_TEMPERATURE``
        - ``LLM_TIMEOUT``
        - ``LLM_MAX_TOKENS``
        - ``<PROVIDER>_API_KEY``
        - ``<PROVIDER>_BASE_URL``
        """

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        provider = (
            provider
            or os.getenv("LLM_PROVIDER")
            or cfg.get("provider", "openai")
        )
        provider_cfg = cfg.get(provider, {})

        model = model or os.getenv("LLM_MODEL") or cfg.get("model")
        temperature = (
            temperature
            if temperature is not None
            else float(os.getenv("LLM_TEMPERATURE", cfg.get("temperature", 0.7)))
        )
        timeout = (
            timeout
            if timeout is not None
            else float(os.getenv("LLM_TIMEOUT", cfg.get("timeout", 30)))
        )
        max_tokens = (
            max_tokens
            if max_tokens is not None
            else int(os.getenv("LLM_MAX_TOKENS", cfg.get("max_tokens", 1024)))
        )

        api_key = (
            api_key
            or os.getenv(f"{provider.upper()}_API_KEY")
            or provider_cfg.get("api_key")
        )
        base_url = (
            base_url
            or os.getenv(f"{provider.upper()}_BASE_URL")
            or provider_cfg.get("base_url")
        )

        return cls(
            provider=provider,
            model=model,
            temperature=temperature,
            timeout=timeout,
            api_key=api_key,
            base_url=base_url,
            max_tokens=max_tokens,
        )

    def generate(
        self,
        prompt: str,
        *,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate a completion for ``prompt`` using the configured provider."""

        provider = provider or self.provider
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        timeout = timeout if timeout is not None else self.timeout
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens

        if provider != "openai":
            raise ValueError(f"Unsupported provider: {provider}")

        try:  # pragma: no cover - import guard
            import openai
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError(
                "openai package is required to generate text"
            ) from exc

        openai.api_key = self.api_key
        if self.base_url:
            openai.base_url = self.base_url

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        return response["choices"][0]["message"]["content"]


__all__ = ["LLMClient"]

