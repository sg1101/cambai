from fastapi import FastAPI, HTTPException
import time
from tasktiger import TaskTiger
import redis
from pydantic import BaseModel
import random

# List of possible sentiments
sentiments = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
topics = ['PRICING', 'CUSTOMER_SERVICE', 'FEATURES']

app = FastAPI()

# Initialize TaskTiger and Redis connections
tiger = TaskTiger()
# redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Dummy storage for task status and statistics (you'll replace this with TaskTiger and Redis)
task_status = {}
statistics = {
    "total_tasks_processed": 0,
    "average_processing_time": 0.0,
    "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0},
    "topic_distribution": {"pricing": 0, "product_features": 0, "customer_service": 0},
}


class FeedbackData(BaseModel):
    feedback_text: str
    platform: str

@app.post("/tasks")
def create_task(task_data: FeedbackData):
    # Enqueue the task for processing
    task_data_dict = task_data.dict()
    task = tiger.delay(process_feedback_task, task_data_dict)

    # Return a response with the task_id (optional)
    return {"task_id": task.id}



# Define a task function that will be executed by the worker
@tiger.task()
def process_feedback_task(task_data):
    # Simulate task processing by waiting for a few seconds (replace with your processing logic)
    time.sleep(5)

    # Update processing statistics in Redis (replace with actual statistics)
    # Example: Increment the total_tasks_processed count
    redis_client.incr('total_tasks_processed')
    redis_client.incr(task_data['platform'].upper())
    # Choose a sentiment randomly
    random_sentiment = random.choice(sentiments)
    redis_client.hincrby('sentiment_distribution', random_sentiment, 1)
    # Example: Update topic distribution
    random_topic = random.choice(topics) # Replace with actual topic categorization logic
    redis_client.hincrby('topic_distribution', random_topic, 1)


# Start the worker to process tasks from the TaskTiger queue
if __name__ == '__main__':
    pass
#
#
#
#
#
#
#
#
#
#
#
# @app.get("/tasks/{task_id}")
# def read_task(task_id: int):
#     """
#     Retrieve the status of a processing task.
#     This endpoint should check the status of the task with the given task_id.
#     """
#     if task_id not in task_status:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"task_id": task_id, "status": task_status[task_id]}
#
# @app.get("/statistics")
# def read_statistics():
#     """
#     Retrieve statistics about the processing, including the number of tasks processed, average processing time,
#     sentiment distribution, and topic distribution.
#     """
#     return statistics

