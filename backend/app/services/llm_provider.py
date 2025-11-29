import requests
import json
from typing import Optional
from ..config import settings


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def call(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Gemini API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or settings.GEMINI_API_KEY)
        if not self.api_key:
            raise ValueError("Gemini API key is required")
    
    def call(self, system_prompt: str, user_prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={self.api_key}"
        
        full_prompt = system_prompt.strip() + "\n\nUser prompt:\n" + user_prompt.strip()
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ]
        }
        
        resp = requests.post(
            url,
            json=payload,
            timeout=(settings.CONNECT_TIMEOUT, settings.READ_TIMEOUT)
        )
        resp.raise_for_status()
        data = resp.json()
        
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise ValueError(f"Unexpected Gemini response: {json.dumps(data, ensure_ascii=False, indent=2)}")


class GrokProvider(LLMProvider):
    """Grok (xAI) API provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or settings.XAI_API_KEY)
        if not self.api_key:
            raise ValueError("xAI API key is required")
    
    def call(self, system_prompt: str, user_prompt: str) -> str:
        url = "https://api.x.ai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ]
        
        payload = {
            "model": settings.GROK_MODEL,
            "messages": messages
        }
        
        resp = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=(settings.CONNECT_TIMEOUT, settings.READ_TIMEOUT)
        )
        resp.raise_for_status()
        data = resp.json()
        
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise ValueError(f"Unexpected Grok response: {json.dumps(data, ensure_ascii=False, indent=2)}")


def get_llm_provider(backend: str, gemini_key: Optional[str] = None, xai_key: Optional[str] = None) -> LLMProvider:
    """Factory function to get LLM provider"""
    if backend == "gemini":
        return GeminiProvider(gemini_key)
    elif backend == "grok":
        return GrokProvider(xai_key)
    else:
        raise ValueError(f"Unknown backend: {backend}")
