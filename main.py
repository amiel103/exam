from fastapi import FastAPI, HTTPException  # Fixed import
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)

USERS_FILE = "users.csv"

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
    if not os.path.exists(USERS_FILE):
        raise HTTPException(status_code=500, detail="User database not found")

    with open(USERS_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row if present
        for row in reader:
            if len(row) == 2 and row[0].strip() == user.username and row[1].strip() == user.password:
                return {"status": "Logged in"}
    
    raise HTTPException(status_code=401, detail="Invalid username or password")


// implemented by Genheylou Felisilda
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
