import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def chat_with_ai(user_message):
    """
    Chat assistant function with Indeyx branding awareness.
    It provides detailed, natural responses about Indeyx and
    short conversational responses otherwise.
    """

    # If user directly asks who built it
    trigger_keywords = ["who built you", "who created you", "who made you"]
    if any(keyword.lower() in user_message.lower() for keyword in trigger_keywords):
        return "I was built by the Indeyx AI Development Team."

    # Full context for Indeyx (acts like company memory)
    indeyx_context = """
Indeyx is a global digital agency specializing in Web Design, Mobile App Development, SaaS Development, 
Software Development, AI Product Development, Business Automation, Brand Identity, 
Digital Marketing, Branding & Packaging, and Pitch Deck Design.

At Indeyx, we turn ideas into impactful digital experiences—from websites and mobile apps to SaaS platforms,
custom software, and automation systems. Our creative team also designs brand identity, digital marketing,
and pitch decks that help businesses stand out and scale.

📍 Offices:
- USA Office: United States, Virginia, Richmond, Downtown
- Pakistan Office: Sindh, Karachi, PECHS, Block 2
📞 Phone: +1 (430) 290-0558
🌐 Website: indeyx.com

Our services include:
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

    # Check if user is asking about Indeyx
    if "indeyx" in user_message.lower():
        context_message = f"The user is asking about Indeyx. Use the following company info:\n\n{indeyx_context}\n\nUser message: {user_message}"
    else:
        context_message = user_message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful AI assistant. If asked about Indeyx, answer accurately using this context: {indeyx_context}"},
                {"role": "user", "content": context_message},
            ],
            temperature=0.7,
            max_tokens=450,  # longer limit for company questions
        )

        ai_reply = response.choices[0].message.content.strip()
        return ai_reply

    except Exception as e:
        print(f"Error in chat AI: {e}")
        return "Sorry, something went wrong while processing your request."
