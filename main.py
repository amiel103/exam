from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
 
# Implemented by Jezzel Faith Q. Gier
@app.post("/login/")
async def user_login(user: User):
    # Implemented by Jezzel
    """
    Handles the user login process. The function checks if the user exists in the users CSV file.
    If the username and password match, the user is logged in successfully.

    Args:
        user (User): The username and password provided by the user.

    Returns:
        dict: A response indicating whether the login was successful or not.
              - If successful, status will be "Logged in".
              - If failed, appropriate message will be returned.
    """

# implemented by Genheylou Felisilda
@app.post("/create_user/")
async def create_user(User: User):
    # my answer here .. .. . . .
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
# implemented by Aubrey
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
    # Implemented by Kimberly Vocales
    """
    Retrieves the list of tasks associated with a specific user.

    Args:
        name (str): The username for which the tasks need to be fetched.

    Returns:
        dict: A list of tasks (task description, deadline, user) associated with the given user.
              - If tasks are found, the response will include the task details.
              - If no tasks are found for the user, an empty list will be returned.
    """
    tasks = []
    tasks_file = 'data/tasks.csv'

    if not os.path.exists(tasks_file):
        return {"tasks": []}

    with open(tasks_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user'] == name:
                tasks.append([row['task'], row['deadline'], row['user']])

    return {"tasks": tasks}

