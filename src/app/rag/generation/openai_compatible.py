from __future__ import annotations

import httpx


class OpenAICompatibleGenerator:
    """Generator for APIs implementing the OpenAI chat-completions contract."""

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str | None = None,
        timeout: float = 300.0,
        supports_system_role: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        self.supports_system_role = supports_system_role

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        if self.supports_system_role:
            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ]
        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{system_prompt}\n\n"
                        "--- BEGIN USER REQUEST ---\n"
                        f"{user_prompt}\n"
                        "--- END USER REQUEST ---"
                    ),
                }
            ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 256,
        }

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        if response.is_error:
            raise RuntimeError(
                f"LLM request failed with HTTP {response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "LLM response did not contain choices[0].message.content."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("LLM returned an empty response.")

        return content.strip()