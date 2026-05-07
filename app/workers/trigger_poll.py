from app.workers.tasks import poll_gmail
from loguru import logger

def trigger_poll():
    logger.info("Manually triggering Gmail poll task...")
    result = poll_gmail.delay()
    logger.info(f"Task triggered with ID: {result.id}")
    logger.info("Check Flower (http://localhost:5555) or worker logs for progress.")

if __name__ == "__main__":
    trigger_poll()
