import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.services.prefilter_service import prefilter_service
from app.services.notifier_service import notifier_service
from app.workflows.state import EmailState
from loguru import logger

# Initialize LLM with Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.GROQ_API_KEY,
    temperature=0
)

def prefilter_node(state: EmailState) -> Dict[str, Any]:
    """
    Wraps the keyword-based prefilter service.
    """
    logger.info(f"Node: Prefilter - Processing email {state['email_data'].get('id')}")
    is_useful = prefilter_service.is_interview_related(state["email_data"])
    return {"is_useful": is_useful}

def classify_node(state: EmailState) -> Dict[str, Any]:
    """
    Uses LLM to categorize the email.
    """
    logger.info(f"Node: Classify - Processing email {state['email_data'].get('id')}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert career assistant. Classify the following email into one of these categories: INTERVIEW, ASSESSMENT, RECRUITER_OUTREACH, APPLICATION_UPDATE, OFFER, REJECTION, NETWORKING, FOLLOW_UP, JOB_MARKETING, NEWSLETTER, SPAM, IGNORE. Return only the category name in uppercase."),
        ("user", "Subject: {subject}\n\nSnippet: {snippet}\n\nBody: {body}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "subject": state["email_data"].get("subject"),
        "snippet": state["email_data"].get("snippet"),
        "body": state["email_data"].get("body")[:2000]  # Truncate body for tokens
    })
    
    category = response.content.strip().upper()
    logger.info(f"Email classified as: {category}")
    
    # Decide if action is required based on category
    actionable_categories = ["INTERVIEW", "ASSESSMENT", "OFFER", "RECRUITER_OUTREACH", "APPLICATION_UPDATE", "FOLLOW_UP"]
    is_useful = category in actionable_categories
    
    return {"category": category, "is_useful": is_useful}

def extract_node(state: EmailState) -> Dict[str, Any]:
    """
    Uses LLM to extract structured entities.
    """
    logger.info(f"Node: Extract - Processing email {state['email_data'].get('id')}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the following entities from the email in JSON format: company_name, role, interview_date, action_required (boolean), urgency (low, medium, high). If an entity is not found, use null. Return ONLY the JSON object, no other text."),
        ("user", "Subject: {subject}\n\nBody: {body}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "subject": state["email_data"].get("subject"),
        "body": state["email_data"].get("body")[:3000]
    })
    
    try:
        content = response.content.strip()
        # More robust JSON extraction
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        entities = json.loads(content)
    except Exception as e:
        logger.warning(f"Failed to parse entities JSON from LLM: {e}. Raw content: {response.content}")
        entities = {}
        
    return {"entities": entities}

def summarize_node(state: EmailState) -> Dict[str, Any]:
    """
    Uses LLM to generate a concise summary.
    """
    logger.info(f"Node: Summarize - Processing email {state['email_data'].get('id')}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate a very concise, actionable 1-2 sentence summary of this career-related email."),
        ("user", "Subject: {subject}\n\nBody: {body}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({
        "subject": state["email_data"].get("subject"),
        "body": state["email_data"].get("body")[:2000]
    })
    
    return {"summary": response.content.strip()}

def notify_node(state: EmailState) -> Dict[str, Any]:
    """
    Wraps the notifier service to send the Telegram notification.
    """
    import asyncio
    logger.info(f"Node: Notify - Processing email {state['email_data'].get('id')}")
    
    # Enrich email data with LLM results for the notification
    enriched_data = state["email_data"].copy()
    enriched_data["summary"] = state.get("summary")
    enriched_data["category"] = state.get("category")
    
    entities = state.get("entities")
    if entities:
        entities_str = "\n".join([f"*{k.replace('_', ' ').title()}:* {v}" for k, v in entities.items() if v])
        enriched_data["snippet"] = f"{state.get('summary')}\n\n{entities_str}"
    else:
        enriched_data["snippet"] = state.get("summary")

    try:
        # Check if an event loop is already running
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        if loop.is_running():
            # If loop is already running, we can't use asyncio.run
            # We use a wrapper or just schedule it
            loop.create_task(notifier_service.send_notification(enriched_data))
        else:
            asyncio.run(notifier_service.send_notification(enriched_data))
            
    except Exception as e:
        logger.error(f"Failed to send notification in node: {e}")
        
    return {"notification_sent": True}
