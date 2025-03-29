import os
import csv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Define file paths
TASKS_FILE = "tasks.csv"

# Define Pydantic model
class Task(BaseModel):
    task: str
    deadline: str
    user: str

# Define the create_task endpoint
@app.post("/create_task/")
async def create_task(task: Task):
    """
    Creates a new task by adding the task description, deadline, and associated user to the tasks CSV file.

    Args:
        Task (Task): The task description, deadline, and associated user.

    Returns:
        dict: A response indicating whether the task was successfully created.
              - If successful, the status will be "Task Created".
    """
    # Ensure the tasks.csv file exists
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["task", "deadline", "user"])  # Write header

    # Append the task to tasks.csv
    with open(TASKS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([task.task, task.deadline, task.user])

    return {"status": "Task Created"}
