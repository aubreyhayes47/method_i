"""LLM client utilities."""
from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import json
import urllib.request
import urllib.error


logger = logging.getLogger(__name__)


class CredentialsError(Exception):
    """Raised when required API credentials are missing."""


class LLMProviderError(Exception):
    """Raised when the provider API returns an error response."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"{status_code}: {message}")
        self.status_code = status_code
        self.message = message


@dataclass
class LLMClient:
    """Simple HTTP client for LLM providers with retry/backoff."""

    api_key: Optional[str] = None
    api_url: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.getenv("LLM_API_KEY")
        self.api_url = self.api_url or os.getenv("LLM_API_URL")
        if not self.api_key or not self.api_url:
            raise CredentialsError("LLM_API_KEY and LLM_API_URL must be set")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt: str, **params: Any) -> Dict[str, Any]:
        """Generate text from the remote LLM provider.

        Parameters
        ----------
        prompt: str
            The input text prompt.
        **params: Any
            Additional parameters forwarded to the provider.

        Returns
        -------
        Dict[str, Any]
            Parsed JSON response from the provider.
        """

        payload = {"prompt": prompt, **params}
        data = json.dumps(payload).encode()

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("LLM request attempt=%s payload=%s", attempt, payload)
                req = urllib.request.Request(
                    self.api_url,
                    data=data,
                    headers=self._headers(),
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read().decode()
                    logger.info(
                        "LLM response attempt=%s status=%s", attempt, resp.status
                    )
                    logger.debug("LLM raw response: %s", body)
                    if resp.status >= 400:
                        raise LLMProviderError(resp.status, body)
                    return json.loads(body)
            except (LLMProviderError, urllib.error.URLError) as exc:
                if attempt == self.max_retries:
                    logger.exception("LLM request failed after retries")
                    raise
                backoff = 2 ** (attempt - 1)
                logger.warning(
                    "LLM request error on attempt %s/%s: %s. Retrying in %ss",
                    attempt,
                    self.max_retries,
                    exc,
                    backoff,
                )
                time.sleep(backoff)
        raise RuntimeError("unreachable")
