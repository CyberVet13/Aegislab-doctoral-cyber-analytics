"""
AegisLab UI — OpenAI and Anthropic API wrapper.
- Single interface: call(model_id, messages, **kwargs).
- Reproducibility: temperature, top_p, seed when supported.
"""

import json
from typing import Any, Dict, List, Optional

from .config import load_env, MODEL_IDS, get_root

load_env()

# Model id mapping for API (display name -> provider + id)
OPENAI_PREFIX = "openai:"
ANTHROPIC_PREFIX = "anthropic:"

# Default API model ids per provider (fallbacks)
OPENAI_DEFAULT = "gpt-4o"
ANTHROPIC_DEFAULT = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5 (from API /v1/models)


def _get_api_model_id(display_name: str) -> tuple[str, str]:
    """Return (provider, api_model_id). Provider is 'openai' or 'anthropic'."""
    if "GPT" in display_name or "gpt" in display_name:
        return "openai", MODEL_IDS.get(display_name, OPENAI_DEFAULT)
    if "Opus" in display_name:
        return "anthropic", MODEL_IDS.get(display_name, "claude-opus-4-6")
    if "Sonnet" in display_name:
        return "anthropic", MODEL_IDS.get(display_name, ANTHROPIC_DEFAULT)
    return "anthropic", ANTHROPIC_DEFAULT


class ModelGateway:
    """Call OpenAI or Anthropic; return content and usage metadata."""

    def __init__(self) -> None:
        self._openai = None
        self._anthropic = None

    def _get_openai(self):
        if self._openai is None:
            try:
                import openai
                self._openai = openai
            except ImportError:
                raise RuntimeError("openai package not installed; pip install openai")
        return self._openai

    def _get_anthropic(self):
        if self._anthropic is None:
            try:
                import anthropic
                self._anthropic = anthropic
            except ImportError:
                raise RuntimeError("anthropic package not installed; pip install anthropic")
        return self._anthropic

    def call(
        self,
        model_display_name: str,
        messages: List[Dict[str, str]],
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Invoke LLM. messages: [{"role": "user"|"assistant"|"system", "content": "..."}].
        Returns {"content": str, "model": str, "usage": {...}, "finish_reason": str}.
        """
        provider, api_id = _get_api_model_id(model_display_name)
        if provider == "openai":
            return self._call_openai(api_id, messages, system=system, temperature=temperature, max_tokens=max_tokens, seed=seed)
        return self._call_anthropic(api_id, messages, system=system, temperature=temperature, max_tokens=max_tokens)

    def _call_openai(
        self,
        model_id: str,
        messages: List[Dict[str, str]],
        *,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        import os
        client = self._get_openai().OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        msgs = list(messages)
        if system:
            msgs = [{"role": "system", "content": system}] + msgs
        kwargs = {
            "model": model_id,
            "messages": msgs,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if seed is not None:
            kwargs["seed"] = seed
        r = client.chat.completions.create(**kwargs)
        choice = r.choices[0] if r.choices else None
        content = choice.message.content if choice else ""
        return {
            "content": content,
            "model": r.model or model_id,
            "usage": {
                "prompt_tokens": getattr(r.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(r.usage, "completion_tokens", 0),
                "total_tokens": getattr(r.usage, "total_tokens", 0),
            },
            "finish_reason": getattr(choice, "finish_reason", None) or "unknown",
        }

    def _call_anthropic(
        self,
        model_id: str,
        messages: List[Dict[str, str]],
        *,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        import os
        client = self._get_anthropic().Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        # Anthropic: system separate; messages user/assistant only
        sys = system or ""
        msgs = [m for m in messages if m.get("role") != "system"]
        for m in messages:
            if m.get("role") == "system":
                sys += "\n" + m.get("content", "")
        kwargs = {
            "model": model_id,
            "max_tokens": max_tokens,
            "messages": msgs,
        }
        if sys.strip():
            kwargs["system"] = sys.strip()
        if temperature is not None:
            kwargs["temperature"] = temperature
        r = client.messages.create(**kwargs)
        text = ""
        if r.content:
            for block in r.content:
                if hasattr(block, "text"):
                    text += block.text
        return {
            "content": text,
            "model": getattr(r, "model", None) or getattr(r, "model_id", None) or model_id,
            "usage": {
                "prompt_tokens": getattr(r.usage, "input_tokens", 0),
                "completion_tokens": getattr(r.usage, "output_tokens", 0),
                "total_tokens": getattr(r.usage, "input_tokens", 0) + getattr(r.usage, "output_tokens", 0),
            },
            "finish_reason": r.stop_reason or "unknown",
        }
