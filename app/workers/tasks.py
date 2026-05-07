from app.core.celery_app import celery_app
from loguru import logger
import time

@celery_app.task(name="app.workers.tasks.poll_gmail")
def poll_gmail():
    logger.info("Polling Gmail for new emails...")
    # This will be implemented later
    return "Gmail polling initiated."
