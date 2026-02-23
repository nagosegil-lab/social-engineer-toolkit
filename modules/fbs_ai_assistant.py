#!/usr/bin/env python
from __future__ import print_function

import json
import os

import requests

try:
    from getpass import getpass
except ImportError:
    getpass = None

try:
    input = raw_input
except NameError:
    pass


MAIN = "AI Assistant for FBS (Facebook Business Suite)"
AUTHOR = "Cursor AI"

DEFAULT_AI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_AI_MODEL = "gpt-4o-mini"
DEFAULT_GRAPH_VERSION = "v21.0"


class FbsAiError(Exception):
    """Custom error for AI/FBS module failures."""


def _ask(prompt, default=None):
    if default:
        message = "{} [{}]: ".format(prompt, default)
    else:
        message = "{}: ".format(prompt)
    value = input(message).strip()
    if not value and default is not None:
        return default
    return value


def _ask_secret(prompt, env_value):
    if env_value:
        return env_value

    if getpass:
        value = getpass("{}: ".format(prompt)).strip()
    else:
        value = input("{}: ".format(prompt)).strip()
    return value


def _build_post_prompt(business_name, product, audience, tone, goal):
    return (
        "Create one short Facebook post in Hebrew for a business.\n"
        "Business: {0}\n"
        "Product or service: {1}\n"
        "Target audience: {2}\n"
        "Tone: {3}\n"
        "Goal / call to action: {4}\n\n"
        "Return only the post text with no extra explanations."
    ).format(business_name, product, audience, tone, goal)


def _parse_ai_response(payload):
    choices = payload.get("choices", [])
    if not choices:
        raise FbsAiError("AI response has no choices.")

    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise FbsAiError("AI response has empty content.")
    return content.strip()


def generate_post(ai_api_key, ai_model, user_prompt, ai_base_url):
    url = ai_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": "Bearer " + ai_api_key,
        "Content-Type": "application/json",
    }
    data = {
        "model": ai_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a Hebrew marketing copywriter.",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            timeout=60,
        )
    except requests.RequestException as exc:
        raise FbsAiError("Failed to reach AI endpoint: {0}".format(exc))

    if response.status_code >= 400:
        raise FbsAiError(
            "AI request failed ({0}): {1}".format(response.status_code, response.text)
        )

    try:
        payload = response.json()
    except ValueError:
        raise FbsAiError("AI response is not valid JSON.")

    return _parse_ai_response(payload)


def publish_to_fbs(page_id, access_token, message, graph_version):
    url = "https://graph.facebook.com/{0}/{1}/feed".format(graph_version, page_id)
    data = {
        "message": message,
        "access_token": access_token,
    }

    try:
        response = requests.post(url, data=data, timeout=60)
    except requests.RequestException as exc:
        raise FbsAiError("Failed to reach Facebook API: {0}".format(exc))

    if response.status_code >= 400:
        raise FbsAiError(
            "Facebook publish failed ({0}): {1}".format(
                response.status_code, response.text
            )
        )

    try:
        payload = response.json()
    except ValueError:
        raise FbsAiError("Facebook response is not valid JSON.")

    post_id = payload.get("id")
    if not post_id:
        raise FbsAiError("Facebook response does not include a post id.")
    return post_id


def main():
    print("\n----------------------------------------------")
    print(" AI + FBS Assistant (Facebook Business Suite)")
    print("----------------------------------------------\n")
    print("This module generates a Facebook post with AI")
    print("and can publish it directly to your Page.\n")

    ai_base_url = _ask(
        "AI base URL",
        os.getenv("AI_BASE_URL", DEFAULT_AI_BASE_URL),
    )
    ai_model = _ask(
        "AI model",
        os.getenv("AI_MODEL", DEFAULT_AI_MODEL),
    )
    ai_api_key = _ask_secret("AI API key", os.getenv("AI_API_KEY"))

    if not ai_api_key:
        print("\n[!] AI API key is required.")
        input("\nPress <enter> to continue")
        return

    business_name = _ask("Business name")
    product = _ask("Product / service")
    audience = _ask("Target audience")
    tone = _ask("Tone", "friendly and professional")
    goal = _ask("Goal / CTA", "Send us a message for details")

    user_prompt = _build_post_prompt(
        business_name,
        product,
        audience,
        tone,
        goal,
    )

    try:
        post_text = generate_post(
            ai_api_key=ai_api_key,
            ai_model=ai_model,
            user_prompt=user_prompt,
            ai_base_url=ai_base_url,
        )
    except FbsAiError as exc:
        print("\n[!] {0}".format(exc))
        input("\nPress <enter> to continue")
        return

    print("\n[+] Suggested post:\n")
    print(post_text)

    publish_choice = _ask("\nPublish to Facebook now? (y/n)", "n").lower()
    if publish_choice != "y":
        print("\n[*] Done. Copy the post text into FBS when ready.")
        input("\nPress <enter> to continue")
        return

    page_id = _ask("Facebook Page ID", os.getenv("FBS_PAGE_ID", ""))
    access_token = _ask_secret(
        "Facebook Page access token",
        os.getenv("FBS_ACCESS_TOKEN"),
    )
    graph_version = _ask(
        "Graph API version",
        os.getenv("FBS_GRAPH_VERSION", DEFAULT_GRAPH_VERSION),
    )

    if not page_id or not access_token:
        print("\n[!] Page ID and Page access token are required for publish.")
        input("\nPress <enter> to continue")
        return

    try:
        post_id = publish_to_fbs(
            page_id=page_id,
            access_token=access_token,
            message=post_text,
            graph_version=graph_version,
        )
    except FbsAiError as exc:
        print("\n[!] {0}".format(exc))
        input("\nPress <enter> to continue")
        return

    print("\n[+] Published successfully. Post ID: {0}".format(post_id))
    input("\nPress <enter> to continue")
