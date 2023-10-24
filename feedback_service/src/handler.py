import json
import uuid

from fastapi import HTTPException

from .models import FeedbackData, ProcessingStatistics
from .config import redis_client
from .workers import process_feedback_task

def create_task(task_data: FeedbackData):
    # Enqueue the task for processing
    task_data_dict = task_data.dict()
    # Generate a unique task ID
    task_data_dict['task_id'] = str(uuid.uuid4())
    # task = tiger.delay(process_feedback_task, task_data_dict)
    process_feedback_task.delay(task_data_dict)

    # # Return a response with the task_id (optional)
    return {"task_id": task_data_dict['task_id']}


def get_task_status(task_id: str):
    # Retrieve the task status from Redis
    task_status_data = redis_client.get(f'task_status:{task_id}')
    if task_status_data:
        return json.loads(task_status_data)
    else:
        raise HTTPException(status_code=404, detail="Task not found")


def get_processing_statistics():
    # Retrieve statistics from Redis
    total_tasks_processed = redis_client.get('total_tasks_processed')
    if total_tasks_processed is not None:
        total_tasks_processed = int(total_tasks_processed)
    else:
        total_tasks_processed = None

    average_processing_time = redis_client.get('average_processing_time')
    if average_processing_time is not None:
        average_processing_time = float(average_processing_time)
    else:
        average_processing_time = None

    # Retrieve sentiment_distribution and topic_distribution as dictionaries
    sentiment_distribution_raw = redis_client.hgetall('sentiment_distribution')
    topic_distribution_raw = redis_client.hgetall('topic_distribution')
    platform_distribution = redis_client.hgetall('platform_distribution')

    statistics = ProcessingStatistics(
        total_tasks_processed=total_tasks_processed,
        average_processing_time=average_processing_time,
        sentiment_distribution=sentiment_distribution_raw,
        topic_distribution=topic_distribution_raw,
        platform_distribution=platform_distribution
    )
    return statistics.dict()