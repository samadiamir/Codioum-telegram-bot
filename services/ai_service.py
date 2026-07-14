from openai import OpenAI
from config.settings import AI_MODEL, AI_BASE_URL, AI_KEY
from utils.logger import log_error, log_warning, log_debug

if not AI_KEY or not AI_MODEL or not AI_BASE_URL:
    log_error("AI configuration is incomplete. Check AI_KEY, AI_MODEL, and AI_BASE_URL in settings.")

client = OpenAI(base_url=AI_BASE_URL, api_key=AI_KEY)


def get_ai_response(user_message, conversation_history=None, system_context=None):
    """
    Get response from AI model with error handling and conversation history.

    Args:
        user_message (str): The user's message
        conversation_history (list): Previous conversation messages for context

    Returns:
        str: AI response or None on error
    """
    if not user_message or not isinstance(user_message, str):
        log_warning("Invalid user message received.")
        return None

    try:
        log_debug(f"Processing AI request for user message: {user_message[:50]}...")

        # Build messages list
        messages = conversation_history if conversation_history else []
        if not isinstance(messages, list):
            log_warning("Conversation history is not a list, resetting to empty.")
            messages = []

        messages.append({"role": "user", "content": user_message})
        if system_context:
            messages.insert(0, {"role": "system", "content": system_context})

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=messages,
        )

        if not response or not response.choices:
            log_warning("Empty response from AI API.")
            return None

        ai_response = response.choices[0].message.content
        log_debug("AI response generated successfully.")
        return ai_response

    except AttributeError as e:
        log_error("Attribute error in AI service (likely invalid config)", e)
        return None
    except Exception as e:
        log_error("AI API Error on first attempt", e)

        # Retry once on error
        try:
            log_debug("Retrying AI request...")
            messages = conversation_history if conversation_history else []
            messages.append({"role": "user", "content": user_message})
            if system_context:
                messages.insert(0, {"role": "system", "content": system_context})

            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )

            if response and response.choices:
                ai_response = response.choices[0].message.content
                log_debug("AI response generated on retry.")
                return ai_response

            log_warning("Retry returned empty response.")
            return None

        except Exception as retry_error:
            log_error("AI API Retry Error", retry_error)
            return None
