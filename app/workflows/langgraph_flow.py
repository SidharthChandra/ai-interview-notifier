from langgraph.graph import StateGraph, END
from langgraph.types import RetryPolicy
from langgraph.checkpoint.memory import MemorySaver
from app.workflows.state import EmailState
from app.workflows.nodes import (
    prefilter_node,
    classify_node,
    extract_node,
    summarize_node,
    notify_node
)

# Initialize checkpointer
checkpointer = MemorySaver()

# Define retry policy for API-dependent nodes
api_retry_policy = RetryPolicy(
    max_attempts=3,
    backoff_factor=2.0,
    retry_on=(Exception,)  # In production, you might want to be more specific
)

def should_classify(state: EmailState):
    """
    Conditional edge: check if the prefilter found the email likely useful.
    """
    if state["is_useful"]:
        return "classify"
    return END

def should_extract(state: EmailState):
    """
    Conditional edge: check if the classification found the email actionable.
    """
    if state["is_useful"]:
        return "extract"
    return END

# Initialize the graph
workflow = StateGraph(EmailState)

# Add nodes with retry policies
workflow.add_node("prefilter", prefilter_node)
workflow.add_node("classify", classify_node, retry=api_retry_policy)
workflow.add_node("extract", extract_node, retry=api_retry_policy)
workflow.add_node("summarize", summarize_node, retry=api_retry_policy)
workflow.add_node("notify", notify_node, retry=api_retry_policy)

# Set entry point
workflow.set_entry_point("prefilter")

# Add edges with conditional routing
workflow.add_conditional_edges(
    "prefilter",
    should_classify,
    {
        "classify": "classify",
        END: END
    }
)

workflow.add_conditional_edges(
    "classify",
    should_extract,
    {
        "extract": "extract",
        END: END
    }
)

# Linear flow for actionable emails
workflow.add_edge("extract", "summarize")
workflow.add_edge("summarize", "notify")
workflow.add_edge("notify", END)

# Compile the graph with checkpointer
app_workflow = workflow.compile(checkpointer=checkpointer)
