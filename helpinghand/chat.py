import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

COMPANY_INFO = """
Helping Hand is a leading home healthcare marketplace. 
Services offered:
- Nursing Care: Professional nurses for post-operative, chronic, or critical care.
- Home Care: Compassionate caregivers for daily assistance and elderly care.
- Medical Services: Physiotherapy, doctor visits, and equipment setup.

Pricing varies by duration. We offer tiered discounts:
- Daily: Base rate
- Weekly: 10% discount
- Monthly: 20% discount

Booking process: Users can search for staff, select their preferred type of service, and book directly through the platform. Only if the user prompts and clicks on the final 'Book now' button will the booking be confirmed and details appear on the dashboard.
"""

def get_chatbot_response(user_message: str, base64_image: str = None, page_context: str = None, history: list = None) -> str:
    llm = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.5-flash",
        temperature=0.3,
    )

    system_prompt_text = (
        "You are the Customer Support and booking assistant for our company called Helping Hand. "
        "Your purpose is to help the user on the platform by understanding their requirements.\n"
        f"You have the following information about the company:\n{COMPANY_INFO}\n"
    )
    
    if page_context:
        system_prompt_text += (
            f"\nAdditionally, the user is currently viewing a webpage with the following scraped text content:\n"
            f'"""\n{page_context}\n"""\n'
            "Use this specific page context to assist them accurately regarding the page they are on.\n"
        )
        
    system_prompt_text += (
        "If the user wants to book a service, actively use the scraped webpage context (which contains service names, descriptions, and pricing) to guide them step-by-step on how to book it. "
        "If the user uploaded an image, scan the image, understand it and assist them based on its context. "
        "Your responses should be short, clear and to the point without any technical or medical jargon. "
        "If the user asks about the pricing, discounts, or any other information, do not make up any numbers, "
        "respond politely from the information you have been provided with earlier."
    )

    messages = [SystemMessage(content=system_prompt_text)]
    
    # Inject conversational history
    if history:
        for msg in history:
            if msg.get('role') == 'user':
                messages.append(HumanMessage(content=msg.get('content', '')))
            elif msg.get('role') == 'assistant':
                messages.append(AIMessage(content=msg.get('content', '')))

    content = [{"type": "text", "text": user_message}]
    if base64_image:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })
        
    messages.append(HumanMessage(content=content))

    response = llm.invoke(messages)
    return response.content

