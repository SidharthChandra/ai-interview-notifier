import base64
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.config import settings
from loguru import logger

class GmailService:
    def __init__(self):
        self.creds = Credentials(
            token=None,
            refresh_token=settings.GOOGLE_REFRESH_TOKEN,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )
        self.service = build("gmail", "v1", credentials=self.creds)

    def fetch_new_emails(self, after_timestamp: datetime):
        """
        Fetch emails received after the given timestamp.
        """
        # Convert timestamp to Gmail query format (seconds since epoch)
        after_epoch = int(after_timestamp.timestamp())
        query = f"after:{after_epoch}"
        
        try:
            results = self.service.users().messages().list(userId="me", q=query).execute()
            messages = results.get("messages", [])
            return messages
        except Exception as e:
            logger.error(f"Error fetching emails from Gmail: {e}")
            return []

    def get_email_details(self, message_id: str):
        """
        Fetch full email content (Subject, Body, Sender).
        """
        try:
            message = self.service.users().messages().get(userId="me", id=message_id, format="full").execute()
            payload = message.get("payload", {})
            headers = payload.get("headers", [])
            
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown Sender")
            
            # Extract body
            body = ""
            if "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        data = part["body"].get("data", "")
                        body = base64.urlsafe_b64decode(data).decode("utf-8")
                        break
            else:
                data = payload["body"].get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
            
            return {
                "id": message_id,
                "subject": subject,
                "sender": sender,
                "body": body,
                "snippet": message.get("snippet", ""),
                "timestamp": int(message.get("internalDate", 0)) / 1000
            }
        except Exception as e:
            logger.error(f"Error fetching email details for {message_id}: {e}")
            return None

gmail_service = GmailService()
