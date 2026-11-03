"""Thin adapters that send one conversation to a vision-language model.

Each adapter takes the provider-neutral messages from conditions.py and
returns the model's reply as plain text. Plain HTTP (requests) is used for
every provider so there are no SDK version problems.

Providers:
  mock     no API, simulated replies (for testing the pipeline only)
  gemini   Google Gemini API      key: GEMINI_API_KEY   (has a free tier)
  openai   OpenAI or any OpenAI-compatible API (OpenRouter, Groq, ...)
           key: OPENAI_API_KEY, or set --base-url and the matching key
  anthropic  Anthropic API        key: ANTHROPIC_API_KEY
  ollama   a model running locally with Ollama (free, no key)
"""

from __future__ import annotations

import base64
import os
import random
import time
from pathlib import Path

import requests

DEFAULT_MODELS = {
    "mock": "mock-v1",
    "gemini": "gemini-2.5-flash",
    "openai": "gpt-4.1-mini",
    "anthropic": "claude-haiku-5-5",
    "ollama": "qwen2.5vl:7b",
}

TIMEOUT = 120


class ModelError(RuntimeError):
    pass


def _b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def _post(url: str, headers: dict, payload: dict, retries: int = 4) -> dict:
    """POST with exponential backoff on rate limits and server errors."""
    delay = 5.0
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise ModelError(f"Network error: {e}") from e
            print(f"    network error, retrying in {delay:.0f}s ...", flush=True)
            time.sleep(delay)
            delay *= 2
            continue
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 529) and attempt < retries - 1:
            why = {429: "rate limit", 503: "model busy"}.get(r.status_code, "server error")
            print(f"    HTTP {r.status_code} ({why}), retrying in {delay:.0f}s ...", flush=True)
            time.sleep(delay)
            delay *= 2
            continue
        raise ModelError(f"HTTP {r.status_code}: {r.text[:500]}")
    raise ModelError("Retries exhausted")


class Model:
    provider = "base"

    def __init__(self, model: str):
        self.model = model

    def complete(self, messages: list[dict], meta: dict | None = None) -> str:
        raise NotImplementedError


class MockModel(Model):
    """Simulated model so the whole pipeline can run without any API key.

    It "reads" the chart correctly most of the time and follows a
    contradicting claim at a different rate for each claim source. These
    numbers are invented. Never report mock output as a finding.
    """

    provider = "mock"
    FOLLOW_RATE = {
        "chart_only": 0.0, "caption": 0.25, "user_claim": 0.40, "user_opinion": 0.15,
        "user_expert": 0.50, "prior_assistant": 0.55, "self_caption": 0.20,
        "self_caption_noclaim": 0.0,
    }
    READ_ERROR = 0.03

    def __init__(self, model: str, seed: int = 0):
        super().__init__(model)
        self.rng = random.Random(seed)

    def complete(self, messages, meta=None):
        if meta is None:
            raise ModelError("Mock model needs chart metadata")
        truth, condition, claim_dir = meta["direction"], meta["condition"], meta.get("claim_direction")
        if condition == "describe":
            verb = "rises" if truth == "increase" else "declines"
            return f"The {meta['metric']} {verb} steadily from {meta['start_label']} to {meta['end_label']}."
        answer = truth
        if self.rng.random() < self.READ_ERROR:
            answer = "decrease" if truth == "increase" else "increase"
        if claim_dir and claim_dir != truth and self.rng.random() < self.FOLLOW_RATE[condition]:
            answer = claim_dir
        if claim_dir and answer == truth and claim_dir != truth and self.rng.random() < 0.5:
            expl = "The chart shows the opposite of the stated claim, so I rely on the plotted values."
        else:
            expl = f"The values {'rise' if answer == 'increase' else 'fall'} across the period."
        if self.rng.random() < 0.02:
            return f"I think it went {'up' if answer == 'increase' else 'down'}."  # unparseable-ish reply
        return '{"answer": "%s", "explanation": "%s"}' % (answer, expl)


class GeminiModel(Model):
    provider = "gemini"

    def __init__(self, model: str):
        super().__init__(model)
        self.key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not self.key:
            raise ModelError("Set GEMINI_API_KEY (free key at aistudio.google.com)")

    def complete(self, messages, meta=None):
        contents = []
        for m in messages:
            parts = []
            for c in m["content"]:
                if c["type"] == "text":
                    parts.append({"text": c["text"]})
                else:
                    parts.append({"inline_data": {"mime_type": "image/png", "data": _b64(c["path"])}})
            contents.append({"role": "model" if m["role"] == "assistant" else "user", "parts": parts})
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        data = _post(
            url,
            {"x-goog-api-key": self.key, "Content-Type": "application/json"},
            {"contents": contents, "generationConfig": {"temperature": 0, "maxOutputTokens": 1024}},
        )
        try:
            parts = data["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts if not p.get("thought"))
        except (KeyError, IndexError) as e:
            raise ModelError(f"Unexpected Gemini response: {str(data)[:500]}") from e


class OpenAIModel(Model):
    """OpenAI chat completions, or any compatible endpoint via base_url."""

    provider = "openai"

    def __init__(self, model: str, base_url: str | None = None, key_env: str | None = None):
        super().__init__(model)
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.key = os.environ.get(key_env or "OPENAI_API_KEY")
        if not self.key:
            raise ModelError(f"Set {key_env or 'OPENAI_API_KEY'}")

    def complete(self, messages, meta=None):
        out = []
        for m in messages:
            if m["role"] == "assistant":
                out.append({"role": "assistant", "content": " ".join(c["text"] for c in m["content"])})
                continue
            parts = []
            for c in m["content"]:
                if c["type"] == "text":
                    parts.append({"type": "text", "text": c["text"]})
                else:
                    parts.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{_b64(c['path'])}"}})
            out.append({"role": "user", "content": parts})
        payload = {"model": self.model, "messages": out, "temperature": 0}
        data = _post(
            f"{self.base_url}/chat/completions",
            {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            payload,
        )
        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError) as e:
            raise ModelError(f"Unexpected response: {str(data)[:500]}") from e


class AnthropicModel(Model):
    provider = "anthropic"

    def __init__(self, model: str):
        super().__init__(model)
        self.key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.key:
            raise ModelError("Set ANTHROPIC_API_KEY")

    def complete(self, messages, meta=None):
        out = []
        for m in messages:
            parts = []
            for c in m["content"]:
                if c["type"] == "text":
                    parts.append({"type": "text", "text": c["text"]})
                else:
                    parts.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": _b64(c["path"])}})
            out.append({"role": m["role"], "content": parts})
        data = _post(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": self.key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": self.model, "max_tokens": 300, "temperature": 0, "messages": out},
        )
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


class OllamaModel(Model):
    provider = "ollama"

    def __init__(self, model: str, base_url: str | None = None):
        super().__init__(model)
        self.base_url = (base_url or os.environ.get("OLLAMA_HOST") or "http://localhost:11434").rstrip("/")

    def complete(self, messages, meta=None):
        out = []
        for m in messages:
            text = "\n".join(c["text"] for c in m["content"] if c["type"] == "text")
            images = [_b64(c["path"]) for c in m["content"] if c["type"] == "image"]
            msg = {"role": m["role"], "content": text}
            if images:
                msg["images"] = images
            out.append(msg)
        data = _post(
            f"{self.base_url}/api/chat",
            {"Content-Type": "application/json"},
            {"model": self.model, "messages": out, "stream": False, "options": {"temperature": 0}},
        )
        return data.get("message", {}).get("content", "")


def get_model(provider: str, model: str | None = None, base_url: str | None = None, key_env: str | None = None) -> Model:
    model = model or DEFAULT_MODELS.get(provider)
    if provider == "mock":
        return MockModel(model)
    if provider == "gemini":
        return GeminiModel(model)
    if provider == "openai":
        return OpenAIModel(model, base_url=base_url, key_env=key_env)
    if provider == "anthropic":
        return AnthropicModel(model)
    if provider == "ollama":
        return OllamaModel(model, base_url=base_url)
    raise ValueError(f"Unknown provider: {provider}")
