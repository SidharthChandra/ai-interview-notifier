from datetime import datetime, timedelta, timezone
import redis
from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.gmail_service import gmail_service
from app.workflows.langgraph_flow import app_workflow
from loguru import logger

# Initialize Redis client for checkpointing
redis_client = redis.from_url(settings.REDIS_URL)

@celery_app.task(name="app.workers.tasks.poll_gmail")
def poll_gmail():
    """
    Poll Gmail for new emails and process them through the LangGraph workflow.
    """
    logger.info("Starting Gmail poll cycle (LangGraph Edition)...")
    
    # 1. Get last poll timestamp from Redis
    last_poll_key = "last_poll_timestamp"
    last_poll_str = redis_client.get(last_poll_key)
    
    if last_poll_str:
        last_poll_ts = datetime.fromisoformat(last_poll_str.decode("utf-8"))
    else:
        # Default to 5 minutes ago if no checkpoint exists
        last_poll_ts = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    logger.info(f"Fetching emails received after: {last_poll_ts.isoformat()}")
    
    # 2. Fetch new emails
    messages = gmail_service.fetch_new_emails(last_poll_ts)
    logger.info(f"Found {len(messages)} new messages to process.")
    
    processed_count = 0
    
    # 3. Process each email
    for msg in messages:
        msg_id = msg["id"]
        
        # Check if we've already processed this message (deduplication)
        dedup_key = f"processed_email:{msg_id}"
        if redis_client.exists(dedup_key):
            continue
            
        # Fetch full details
        email_data = gmail_service.get_email_details(msg_id)
        if not email_data:
            continue
            
        processed_count += 1
        
        # 4. Run LangGraph Workflow
        logger.info(f"Invoking LangGraph for email: {msg_id}")
        try:
            # Use thread_id for checkpointing (unique per email)
            config = {"configurable": {"thread_id": msg_id}}
            
            app_workflow.invoke({
                "email_data": email_data,
                "is_useful": False,
                "category": None,
                "entities": None,
                "summary": None,
                "notification_sent": False
            }, config=config)
        except Exception as e:
            logger.error(f"LangGraph workflow failed for email {msg_id}: {e}")
            
        # Mark as processed in Redis (expire after 24 hours)
        redis_client.setex(dedup_key, timedelta(hours=24), "1")
    
    # 6. Update last poll timestamp in Redis
    redis_client.set(last_poll_key, datetime.now(timezone.utc).isoformat())
    
    logger.success(f"Poll cycle complete. Processed: {processed_count}")
    return f"Processed {processed_count} emails through LangGraph."
