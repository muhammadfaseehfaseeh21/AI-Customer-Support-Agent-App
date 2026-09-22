import os
from groq import Groq

# Initialize Groq Client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_agent_response(
    customer_id: str, customer_data: dict, chat_history: list
) -> str:
    """Generate AI response with customer context using Groq and openai/gpt-oss-120b."""
    if not GROQ_API_KEY:
        return "⚠️ Error: GROQ_API_KEY is missing. Please set it in your environment or Streamlit secrets."

    client = Groq(api_key=GROQ_API_KEY)

    # Format customer context for the agent
    context = f"""
    You are an AI Customer Support Agent for an e-commerce platform.
    Always be polite, helpful, clear, and professional.

    Current Customer Details:
    - Customer ID: {customer_id}
    - Name: {customer_data['name']}
    - Email: {customer_data['email']}
    - Shipping Address: {customer_data['address']}
    - Order History: {customer_data['orders']}

    Instructions:
    1. Help the customer with questions about their orders, delivery status, shipping address, or general product inquiries.
    2. Refer to specific order IDs and items when replying to queries about orders.
    3. Do not invent orders or details not present in the customer context.
    """

    # Build messages array
    messages = [{"role": "system", "content": context}]

    # Append recent chat history
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error communicating with Groq API: {str(e)}"
