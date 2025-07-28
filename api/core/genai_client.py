import json
from typing import Any, Dict

import aiohttp

from config.config import config


class SimpleGenAIClient:
    """Memory-optimized single GenAI client"""

    def __init__(self):
        self.provider = config.GENAI_PROVIDER
        self.session = None

    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
            )
        return self.session

    async def generate_response(self, prompt: str, schema: Dict = None) -> Dict[str, Any]:
        """Generate response with active provider"""
        session = await self.get_session()

        if self.provider == "openai" and config.OPENAI_API_KEY:
            return await self._call_openai(session, prompt, schema)
        elif self.provider == "claude" and config.CLAUDE_API_KEY:
            return await self._call_claude(session, prompt, schema)
        else:
            raise ValueError(f"Provider {self.provider} not configured")

    async def _call_openai(self, session, prompt: str, schema: Dict = None):
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.7,
        }

        if schema:
            payload["response_format"] = {"type": "json_object"}
            prompt += f"\n\nPlease respond in valid JSON format matching this schema: {json.dumps(schema)}"
            payload["messages"][0]["content"] = prompt

        async with session.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        ) as response:
            data = await response.json()
            return {
                "content": data["choices"][0]["message"]["content"],
                "provider": "openai",
                "tokens_used": data.get("usage", {}).get("total_tokens", 0),
            }

    async def _call_claude(self, session, prompt: str, schema: Dict = None):
        headers = {
            "x-api-key": config.CLAUDE_API_KEY,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
        }

        if schema:
            prompt += f"\n\nPlease respond in valid JSON format matching this schema: {json.dumps(schema)}"

        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}],
        }

        async with session.post(
            "https://api.anthropic.com/v1/messages", headers=headers, json=payload
        ) as response:
            data = await response.json()
            return {
                "content": data["content"][0]["text"],
                "provider": "claude",
                "tokens_used": data.get("usage", {}).get("input_tokens", 0)
                + data.get("usage", {}).get("output_tokens", 0),
            }

    async def close(self):
        if self.session:
            await self.session.close()


# Global client instance
genai_client = SimpleGenAIClient()
