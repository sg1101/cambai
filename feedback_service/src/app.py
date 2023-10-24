from fastapi import FastAPI

from .handler import create_task, get_task_status, get_processing_statistics

app = FastAPI()

# API route for submitting a new data processing task
app.add_api_route(path="/tasks", endpoint=create_task, methods=["POST"], response_model=dict)

# API route for retrieving the status of a processing task
app.add_api_route(path="/tasks/{task_id}", endpoint=get_task_status, methods=["GET"], response_model=dict)

# API route for retrieving processing statistics
app.add_api_route(path="/statistics", endpoint=get_processing_statistics, methods=["GET"], response_model=dict)
