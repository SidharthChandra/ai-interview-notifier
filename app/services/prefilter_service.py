from loguru import logger

class PrefilterService:
    INTERVIEW_KEYWORDS = [
        "interview", "scheduling", "invitation", "assessment", 
        "coding test", "technical round", "hiring", "recruiter",
        "offer", "application update", "onboarding"
    ]
    
    IGNORE_KEYWORDS = [
        "job recommendation", "newsletter", "marketing", 
        "promotional", "career advice", "digest"
    ]

    def is_interview_related(self, email_data: dict) -> bool:
        """
        Simple keyword-based filtering to identify high-value career emails.
        """
        subject = email_data.get("subject", "").lower()
        body = email_data.get("body", "").lower()
        snippet = email_data.get("snippet", "").lower()
        
        combined_text = f"{subject} {snippet} {body}"
        
        # Check for ignore keywords first
        for word in self.IGNORE_KEYWORDS:
            if word in combined_text:
                logger.info(f"Email {email_data.get('id')} ignored due to keyword: {word}")
                return False
        
        # Check for interview keywords
        for word in self.INTERVIEW_KEYWORDS:
            if word in combined_text:
                logger.info(f"Email {email_data.get('id')} matched interview keyword: {word}")
                return True
                
        return False

prefilter_service = PrefilterService()
