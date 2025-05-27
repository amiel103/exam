from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

from pydantic import BaseModel

DATABASE_URL="postgresql://airyll_user:iKiLhVkL0nHuRn2BFTsGWdmM4vEQI7Ls@dpg-d0k5tbruibrs73983cs0-a.singapore-postgres.render.com/airyll"
engine = create_engine(DATABASE_URL,  client_encoding='utf8')

connection = engine.connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)
class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str

class TaskCompletion(BaseModel):
    task_id: int
    is_completed: bool


@app.post("/login/")
async def user_login(User: User):

    result = connection.execute(
        text("""
            insert your query here
            """
        )
    )
    """
    Handles the user login process. The function checks if the user exists in the users CSV file.
    If the username and password match, the user is logged in successfully.

    Args:
        User (User): The username and password provided by the user.

    Returns:
        dict: A response indicating whether the login was successful or not.
            - If successful, ttasktatus will be "Logged in".
            - If failed (user not found or incorrect password), appropriate message will be returned.
    """
    return {"status": "Logged in"}


@app.post("/create_user/")
async def create_user(User: User):
    """
    Creates a new user by adding their username and password to the users CSV file.

    Args:
        User (User): The username and password for the new user.

    Returns:
        dict: A response indicating whether the user was successfully created.
            - If successful, the status will be "User Created".
            - If user already exists, a relevant message will be returned.
    """
    return {"status": "User Created"}

@app.post("/create_task/")
async def create_task(Task: Task):
    """
    Creates a new task by adding the task description, deadline, and associated user to the tasks CSV file.

    Args:
        Task (Task): The task description, deadline, and associated user.

    Returns:
        dict: A response indicating whether the task was successfully created.
            - If successful, the status will be "Task Created".
    """
    return {"status": "task Created"}

@app.get("/get_tasks/")
async def get_tasks(name: str):

    """
    Retrieves the list of tasks associated with a specific user.

    Args:
        name (str): The username for which the tasks need to be fetched.

    Returns:
        dict: A list of tasks (task description, deadline) associated with the given user.
            - If tasks are found, the response will include the task details.
            - If no tasks are found for the user, an empty list will be returned.
    """



    return {"tasks": [ ['laba','2','a'] , ['study','6','a'] , ['code','10','a']  ] }

@app.post("/complete_task/")
async def complete_task(data: TaskCompletion):
    """
    Marks a specific task as completed or not completed.

    Args:
        data (Task Completion): Contains task_id and desired is_completed status.

    Returns:
        dict: A response indicating whether the update was successful.
    """
    try:
        # Ensure your database connection and table/column names are correct
        connection.execute(
            text("""
                UPDATE tasks
                SET is_completed = :is_completed
                WHERE id = :task_id
            """),
            {"is_completed": data.is_completed, "task_id": data.task_id}
        )
        connection.commit() # Important for DML operations to save changes
        return {"status": "Task completion updated"}
    except Exception as e:
        # Basic error handling - you might want more specific SQLAlchemy error handling
        print(f"Database error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Internal Server Error during task completion")