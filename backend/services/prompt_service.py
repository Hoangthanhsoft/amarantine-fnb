"""
Prompt Service — Base templates (MIT open source).

Brand voice is pulled from the venue config stored in DB.
Custom venue-specific prompts (e.g. Gambaro) are in the Full Version.
"""


def build_system_prompt(venue: dict) -> str:
    """Build system prompt from venue config."""
    name = venue.get("name", "our venue")
    brand_voice = venue.get("brand_voice") or "Premium quality, authentic experience"
    tone_keywords = venue.get("tone_keywords") or ["premium", "fresh", "authentic"]
    avoid_words = venue.get("avoid_words") or ["cheap", "budget"]

    return f"""You are an expert marketing copywriter for {name},
a premium restaurant/venue.

BRAND VOICE: {brand_voice}
TONE KEYWORDS: {', '.join(tone_keywords)}
NEVER USE THESE WORDS: {', '.join(avoid_words)}

RULES:
- Write in Australian English
- Be specific, not generic
- Feel premium and authentic
- Never use exclamation marks excessively
- Include a subtle call-to-action where appropriate
OUTPUT: Return ONLY valid JSON. No markdown fences."""


CONTENT_PROMPTS = {
    "social_bundle": """
Generate marketing copy for this promotion: "{promo_input}"

Return ONLY valid JSON in this exact format:
{{
  "facebook_posts": ["post1", "post2", "post3"],
  "instagram_caption": "...",
  "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "email_subject_lines": ["sub1", "sub2", "sub3"],
  "email_body": "...",
  "video_script_15s": "...",
  "video_script_30s": "...",
  "signage_headline": "...",
  "signage_subline": "...",
  "menu_description": "...",
  "midjourney_prompt": "...",
  "web_copy": "..."
}}

Guidelines:
- Facebook: 150-200 chars each, 3 different angles (urgency / lifestyle / value)
- Instagram: 100-150 chars, conversational tone
- Email body: 150-200 words, warm and personal
- Video 15s: punchy hook, ends with venue name
- Video 30s: story arc — atmosphere → dish → offer → CTA
- Midjourney: professional food photography prompt with specific lighting and angle
- Signage headline: max 8 words, bold and clear
"""
}


def build_content_prompt(promo_input: str, prompt_type: str = "social_bundle") -> str:
    template = CONTENT_PROMPTS.get(prompt_type)
    if not template:
        raise ValueError(f"Unknown prompt type: {prompt_type}")
    return template.format(promo_input=promo_input)
