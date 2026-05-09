import openai
import anthropic
import logging
from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class AIService:
    """GPT-4o primary + Claude 3.5 Sonnet fallback."""

    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self.anthropic_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        use_fallback: bool = True
    ) -> tuple[str, str]:
        """
        Generate text via GPT-4o. Falls back to Claude on rate limit / error.
        Returns (content, model_used).
        """
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content, "gpt-4o"

        except openai.RateLimitError:
            logger.warning("GPT-4o rate limited — switching to Claude")
            if use_fallback:
                return await self._claude_fallback(system_prompt, user_prompt, max_tokens)
            raise

        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            if use_fallback:
                return await self._claude_fallback(system_prompt, user_prompt, max_tokens)
            raise

    async def _claude_fallback(self, system_prompt: str, user_prompt: str, max_tokens: int) -> tuple[str, str]:
        response = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text, "claude-3-5-sonnet"


ai_service = AIService()
