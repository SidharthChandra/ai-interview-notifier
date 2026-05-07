import httpx
from app.core.config import settings
from loguru import logger

class NotifierService:
    async def send_notification(self, email_data: dict):
        """
        Send a structured notification to Telegram via Bot API.
        """
        if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_bot_token":
            logger.warning("Telegram Bot Token not configured. Skipping notification.")
            return
        
        if not settings.TELEGRAM_CHAT_ID or settings.TELEGRAM_CHAT_ID == "your_chat_id":
            logger.warning("Telegram Chat ID not configured. Skipping notification.")
            return

        subject = email_data.get("subject", "No Subject")
        sender = email_data.get("sender", "Unknown Sender")
        snippet = email_data.get("snippet", "")
        
        # Create a structured message for Telegram
        # Using Markdown (v1) for simplicity
        text = (
            f"*🚀 New Career Opportunity Detected!*\n\n"
            f"*Subject:* {subject}\n"
            f"*From:* {sender}\n"
            f"*Snippet:* {snippet}\n\n"
            f"Please check your Gmail for more details."
        )
        
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.success(f"Notification sent successfully to Telegram for email: {email_data.get('id')}")
        except Exception as e:
            logger.error(f"Failed to send notification to Telegram: {e}")

notifier_service = NotifierService()
