import time
import random

from tasktiger import TaskTiger

from .config import redis_client
from .constants import TaskStatus, sentiments, topics
from .utils import update_task_status

tiger = TaskTiger(connection=redis_client, config={
    'BATCH_QUEUES': {
        # Batch up to 50 tasks that are queued in the my_batch_queue or any
        # of its subqueues, except for the send_email subqueue which only
        # processes up to 10 tasks at a time.
        'my_batch_queue': 50,
        'my_batch_queue.send_email': 10,
    },
})

@tiger.task()
def process_feedback_task(task_data):
    try:
        # Set the task status to 'IN_PROGRESS' at the beginning
        update_task_status(task_data['task_id'], TaskStatus.IN_PROGRESS)

        # Replace with your actual processing logic that takes 5-10 seconds
        processing_time: float = random.uniform(5, 10)
        time.sleep(processing_time)

        # Update processing statistics in Redis based on actual processing results
        # Example: Update sentiment distribution based on sentiment analysis
        sentiment = random.choice(sentiments)  # Replace with actual sentiment analysis

        total_tasks_processed = redis_client.get('total_tasks_processed')
        if total_tasks_processed is None:
            redis_client.set('average_processing_time', processing_time)
            redis_client.set('total_tasks_processed', 1)
        else:
            total_processing_time = float(total_tasks_processed) * float(redis_client.get('average_processing_time'))
            total_processing_time += processing_time
            total_tasks_processed = int(total_tasks_processed) + 1
            redis_client.set('total_tasks_processed', total_tasks_processed)
            redis_client.set('average_processing_time', total_processing_time / total_tasks_processed)

        # redis_client.incr(task_data['platform'].upper())
        redis_client.hincrby('platform_distribution', task_data['platform'].upper(), 1)
        redis_client.hincrby('sentiment_distribution', sentiment, 1)

        # Example: Update topic distribution based on categorization logic
        topic = random.choice(topics)  # Replace with actual categorization logic
        redis_client.hincrby('topic_distribution', topic, 1)

        # Set the task status to 'COMPLETED' when processing is successful
        update_task_status(task_data['task_id'], TaskStatus.COMPLETED)
    except Exception as e:
        # Handle errors and update task status to 'FAILED' with details
        update_task_status(task_data['task_id'], TaskStatus.FAILED, str(e))
        raise e