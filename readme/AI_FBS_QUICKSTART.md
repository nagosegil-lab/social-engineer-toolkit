# AI + FBS Quickstart

This guide explains how to use the SET third-party module:

- `modules/fbs_ai_assistant.py`

The module does two things:

1. Generates a Facebook post with an AI model.
2. Optionally publishes the generated post to a Facebook Page through Graph API.

## 1) Required environment variables

For AI generation:

- `AI_API_KEY` - API key for your AI provider.
- `AI_BASE_URL` - Optional, defaults to `https://api.openai.com/v1`.
- `AI_MODEL` - Optional, defaults to `gpt-4o-mini`.

For publishing to Facebook (optional):

- `FBS_PAGE_ID` - Facebook Page ID.
- `FBS_ACCESS_TOKEN` - Facebook Page access token.
- `FBS_GRAPH_VERSION` - Optional, defaults to `v21.0`.

## 2) Run from SET

1. Start SET.
2. Go to `Third Party Modules`.
3. Select `AI Assistant for FBS (Facebook Business Suite)`.
4. Fill prompts:
   - Business name
   - Product/service
   - Audience
   - Tone
   - Goal/CTA
5. Review the generated post.
6. Choose whether to publish now.

## 3) Notes

- The module does not store your API keys to disk.
- If `AI_BASE_URL` points to an OpenAI-compatible endpoint, the module should work without code changes.
- You are responsible for permissions and compliance for all APIs used.
