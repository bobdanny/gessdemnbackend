import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def gizmotize(user_message):
    """
    Gizmotize AI Assistant
    - Represents Gizmotize (India's Premium Tech Destination)
    - Assists users with products, categories, store info, and brand details
    - Responds in a friendly, premium, and professional tone
    """
              
    # Trigger: Who built you
    creator_keywords = ["who built you", "who created you", "who made you"]
    if any(k in user_message.lower() for k in creator_keywords):
        return "I’m the official AI assistant created for Gizmotize to help you discover premium tech products."

    # Trigger: Assistant name
    name_keywords = ["what is your name", "who are you", "your name"]
    if any(k in user_message.lower() for k in name_keywords):
        return "I’m Gizmo 🤖 — your smart assistant at Gizmotize!"

    # Gizmotize brand & store context
    gizmotize_context = """
Gizmotize is India’s premium tech destination, offering a carefully curated selection of high-end gadgets and accessories.

We specialize in:
- Flagship Smartphones
- Premium Audio Devices
- Smart Home Technology
- Tech Accessories

Why customers choose Gizmotize:
- 1000+ premium products
- 50K+ happy customers with 5-star reviews
- Expert curation of latest technology
- 24/7 customer support
- Physical store experience available

📍 Store Location:
Shop No: 1, 4/66, Saraswati Marg, WEA,
Karol Bagh, Delhi – 110005

📞 Contact: +91 96869 95189  
📧 Email: support@gizmotize.com

Gizmotize brings technology that inspires and elevates everyday life.
"""

    # Product & category-related keywords
    product_keywords = [
        "smartphone", "phone", "iphone", "android",
        "audio", "headphone", "earbuds", "speaker",
        "smart home", "security", "automation",
        "accessories", "charger", "cable", "case",
        "store", "location", "shop", "visit",
        "price", "buy", "purchase", "available"
    ]

    # If user is asking about products or categories
    if any(word in user_message.lower() for word in product_keywords):
        return (
            "Absolutely! 😊 Gizmotize offers a premium selection of gadgets including smartphones, audio devices, smart home products, and accessories.\n\n"
            "You can:\n"
            "🛍️ Browse products by category\n"
            "🏬 Visit our Karol Bagh store for a hands-on experience\n"
            "📞 Contact our team at **+91 96869 95189** for expert guidance\n\n"
            "Tell me what kind of tech you’re looking for, and I’ll help you find the perfect match!"
        )

    # If Gizmotize is mentioned explicitly, enrich the context
    if "gizmotize" in user_message.lower():
        context_message = f"The user is asking about Gizmotize. Use this information:\n\n{gizmotize_context}\n\nUser message: {user_message}"
    else:
        context_message = user_message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly, premium, and knowledgeable AI assistant for Gizmotize. "
                        "Always represent the brand professionally and accurately using this context:\n\n"
                        f"{gizmotize_context}"
                    )
                },
                {"role": "user", "content": context_message},
            ],
            temperature=0.7,
            max_tokens=450,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error in Gizmotize AI Assistant: {e}")
        return "Sorry, I’m having trouble right now. Please try again shortly."
