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

@app.on_event("startup")
async def startup_event():
    """
    Creates the users table if it doesn't exist when the FastAPI application starts.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """))
            conn.commit() # Commit the transaction to ensure table creation is saved
        print("Users table checked/created successfully!")
    except Exception as e:
        print(f"Error creating users table: {e}")
        # You might want to raise the exception or handle it more robustly
        # depending on your application's error handling strategy.

class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str


@app.post("/login/") #airyllsanchez
async def user_login(user: User):
    """
    Handles the user login process. The function checks if the user exists in the users table.
    If the username and password match, the user is logged in successfully.

    Args:
        user (User): A Pydantic model containing:
            - username (str): The username provided by the user.
            - password (str): The corresponding password.

    Returns:
        dict: A response indicating whether the login was successful or not.
            - If successful, the response will be: {"status": "Logged in"}
            - If failed, the response will be: {"status": "Invalid username or password"}
            - If an internal error occurs, the response will include the error detail.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT * FROM users
                    WHERE username = :username AND password = :password
                """),
                {"username": user.username, "password": user.password}
            ).fetchone()

        if result:
            return {"status": "Logged in"}
        else:
            return {"status": "Invalid username or password"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
# This is a simple way to get a user into the DB for testing the login.
@app.on_event("startup")
async def create_test_user():
    try:
        with engine.connect() as conn:
            # Check if a user with 'testuser' already exists
            user_exists = conn.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": "testuser"}
            ).fetchone()

            if not user_exists:
                conn.execute(
                    text("INSERT INTO users (username, password) VALUES (:username, :password)"),
                    {"username": "testuser", "password": "testpassword"}
                )
                conn.commit()
                print("Test user 'testuser' created successfully!")
            else:
                print("Test user 'testuser' already exists.")
    except Exception as e:
        print(f"Error creating test user: {e}")


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