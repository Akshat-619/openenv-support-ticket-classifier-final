import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


def classify_ticket_with_llm(ticket: str) -> str:
    text = ticket.lower()

    if OpenAI is not None:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("API_BASE_URL")
        model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

        if api_key:
            try:
                client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "Classify the ticket as billing, shipping, or technical. Return only one label."
                        },
                        {"role": "user", "content": ticket},
                    ],
                    temperature=0,
                )
                label = response.choices[0].message.content.strip().lower()
                if label in {"billing", "shipping", "technical"}:
                    return label
            except Exception:
                pass

    if any(word in text for word in ["charged", "refund", "payment", "billed"]):
        return "billing"
    if any(word in text for word in ["delivery", "package", "arrived", "address", "shipping"]):
        return "shipping"
    return "technical"