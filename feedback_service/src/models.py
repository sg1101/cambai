from typing import Optional
from pydantic import BaseModel


class FeedbackData(BaseModel):
    feedback_text: str
    platform: str


class TaskStatus(BaseModel):
    task_id: str
    status: str  # You can use 'IN_PROGRESS', 'COMPLETED', 'FAILED', etc.
    details: str


class ProcessingStatistics(BaseModel):
    total_tasks_processed: Optional[int]
    average_processing_time: Optional[float]
    sentiment_distribution: Optional[dict]
    topic_distribution: Optional[dict]
    platform_distribution: Optional[dict]
