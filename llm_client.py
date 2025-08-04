import os
from typing import Optional

import yaml


class LLMClient:
    """Simple LLM client that loads default parameters from a config file."""

    def __init__(self, config_path: str = "config/llm.yaml") -> None:
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f) or {}

        self.api_key = os.getenv("OPENAI_API_KEY")
        # Allow environment variable override for the model
        self.model = os.getenv("LLM_MODEL", self.config.get("model"))
        self.temperature = self.config.get("temperature", 0.7)
        self.max_tokens = self.config.get("max_tokens", 1024)

    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate a completion for the given prompt.

        Parameters can override the defaults loaded from configuration.
        """
        model = model or self.model
        temperature = temperature or self.temperature
        max_tokens = max_tokens or self.max_tokens

        try:
            import openai
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError("openai package is required to generate text") from exc

        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response["choices"][0]["message"]["content"]
