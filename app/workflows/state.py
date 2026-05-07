from typing import TypedDict, Optional, Dict, Any

class EmailState(TypedDict):
    """
    Represents the state of the email processing workflow.
    """
    email_data: Dict[str, Any]
    is_useful: bool
    category: Optional[str]
    entities: Optional[Dict[str, Any]]
    summary: Optional[str]
    notification_sent: bool
