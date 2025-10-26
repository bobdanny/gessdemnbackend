import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def chat_with_cromtek(user_message):
    """
    Cromtek AI Assistant
    - Familiar with Cromtek Solutions Pvt Ltd (cromtek@cromteksolutions.info, +91 8168616807)
    - Responds naturally to inquiries about Cromtek, its services, or domain expertise
    - Offers guidance for potential clients in a professional, friendly tone
    """

    # Keywords that trigger "who built you" replies
    trigger_keywords = ["who built you", "who created you", "who made you"]
    if any(keyword.lower() in user_message.lower() for keyword in trigger_keywords):
        return "I was built by the Cromtek AI Development Team."

    # Keywords that trigger "bot name" reply
    name_keywords = ["what is your name", "who are you", "your name"]
    if any(keyword.lower() in user_message.lower() for keyword in name_keywords):
        return "My name is Myra. 👋"

    # Core Cromtek company context
    cromtek_context = """
Cromtek Solutions Pvt Ltd is a leading digital solutions provider. We specialize in Mobile Applications (iOS, Android, Blackberry, Windows), Web Development, Custom ERP Solutions, Enterprise Solutions, Maintenance and Support, IT Advisory Services, Business Process Transformations, Governance and Compliances, Resource Augmentations, Web3 Solutions with Smart Wallet, Fintech Solutions, Power BI Development, SAP Solutions, Omni Channel Solutions, HRMS and Payroll, School Management Systems, Hospital Management Systems, and other innovative IT solutions.

📞 Phone: +91 8168616807
📧 Email: cromtek@cromteksolutions.info
🌐 Website: https://cromteksolutions.info

We help businesses design, develop, and maintain robust IT systems, mobile apps, and web applications, while optimizing workflows and boosting operational efficiency.
"""

    # Service-related trigger keywords
    service_keywords = [
        "mobile app", "web development", "erp", "enterprise solution", "maintenance",
        "it advisory", "business process", "governance", "resource", "web3", "fintech",
        "power bi", "sap", "omni channel", "hrms", "school management", "hospital management"
    ]

    # Detect if user is asking about a service Cromtek offers
    if any(word in user_message.lower() for word in service_keywords):
        return (
            "Absolutely! Cromtek Solutions can help you with that. 🚀\n\n"
            "We provide end-to-end solutions tailored to your needs — from mobile and web apps to ERP systems, Fintech, and Web3 platforms.\n\n"
            "You can get started by:\n"
            "👉 Visiting our website: **https://cromteksolutions.info**\n"
            "👉 Contacting us directly via phone: **+91 8168616807** or email: **cromtek@cromteksolutions.info**\n\n"
            "Would you like me to explain how we approach this service?"
        )

    # If the message mentions Cromtek, add company context
    if "cromtek" in user_message.lower():
        context_message = f"The user is asking about Cromtek. Use this company info:\n\n{cromtek_context}\n\nUser message: {user_message}"
    else:
        context_message = user_message

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a friendly and professional AI assistant representing Cromtek Solutions Pvt Ltd. "
                               f"If asked about Cromtek or its services, answer accurately using this context: {cromtek_context}"
                },
                {"role": "user", "content": context_message},
            ],
            temperature=0.8,
            max_tokens=450,
        )

        ai_reply = response.choices[0].message.content.strip()
        return ai_reply

    except Exception as e:
        print(f"Error in Cromtek chat AI: {e}")
        return "Sorry, something went wrong while processing your request."
