import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def chat_with_ai(user_message):
    """
    Indeyx AI Assistant
    - Aware of Indeyx branding and services (indeyx.agency)
    - Responds naturally to inquiries about Indeyx or its services
    - Offers human-like support guidance for potential clients
    """

    # Keywords that trigger "who built you" replies
    trigger_keywords = ["who built you", "who created you", "who made you"]
    if any(keyword.lower() in user_message.lower() for keyword in trigger_keywords):
        return "I was built by the Indeyx AI Development Team."

    # Core Indeyx company context
    indeyx_context = """
Indeyx is a global digital agency specializing in Web Design, Mobile App Development, 
SaaS Development, Software Development, AI Product Development, Business Automation, 
Brand Identity, Digital Marketing, Branding & Packaging, and Pitch Deck Design.

At Indeyx, we turn ideas into impactful digital experiences — from websites and mobile apps 
to SaaS platforms, custom software, and automation systems. Our creative team also designs 
brand identity, digital marketing, and pitch decks that help businesses stand out and scale.

📍 Offices:
- USA Office: United States, Virginia, Richmond, Downtown
- Pakistan Office: Sindh, Karachi, PECHS, Block 2

📞 Phone: +1 (430) 290-0558
🌐 Website: indeyx.agency

Our core services:
- Web Design (custom, responsive, and user-friendly)
- Mobile App Development (iOS, Android, UI/UX, optimized builds)
- SaaS Development (dashboards, cloud, scalable systems)
- Business Automation (CRM, workflows, social & eCommerce automation)
- Branding & Packaging (logos, identity kits, full brand visuals)
- Digital Marketing (promo content, campaigns, social management)
- Pitch Deck Design (investor-ready, persuasive designs)

Our slogan: “We turn ideas into stories that stick.”
We’ve served 2000+ satisfied customers across industries globally.
"""

    # Service-related trigger keywords
    service_keywords = [
        "web design", "website", "app", "mobile app", "branding", "logo", "marketing",
        "pitch deck", "automation", "crm", "software", "saas", "ui ux", "ecommerce",
        "digital marketing", "brand", "business automation", "social media"
    ]

    # Detect if user is asking for a service we offer
    if any(word in user_message.lower() for word in service_keywords):
        return (
            "That’s definitely something we can help you with at Indeyx Agency! 🚀\n\n"
            "We specialize in full-service digital solutions — from web design and app development "
            "to branding and automation systems.\n\n"
            "To get started, you can:\n"
            "👉 Visit our website: **https://indeyx.agency**\n"
            "👉 Or reach us directly via WhatsApp or phone: **+1 (430) 290-0558**\n\n"
            "Would you like me to briefly explain how we handle that service?"
        )

    # If message mentions Indeyx, add company context
    if "indeyx" in user_message.lower():
        context_message = f"The user is asking about Indeyx. Use this company info:\n\n{indeyx_context}\n\nUser message: {user_message}"
    else:
        context_message = user_message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a friendly and professional AI assistant representing Indeyx Agency. "
                               f"If asked about Indeyx or its services, answer accurately using this context: {indeyx_context}"
                },
                {"role": "user", "content": context_message},
            ],
            temperature=0.8,
            max_tokens=450,
        )

        ai_reply = response.choices[0].message.content.strip()
        return ai_reply

    except Exception as e:
        print(f"Error in chat AI: {e}")
        return "Sorry, something went wrong while processing your request."
