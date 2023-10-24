import json

from .models import TaskStatus
from .config import redis_client


def update_task_status(task_id, status: TaskStatus, details=None):
    status_data = {"task_id": task_id, "status": status.value}
    if details:
        status_data["details"] = details
    # Use Redis to set the task status with the task_id as the key
    redis_client.set(f'task_status:{task_id}', json.dumps(status_data))
