from fastapi import FastAPI

# Import our custom logic
import app.db_models
from app.database import engine

# -----import routers
from app.routers import tasks, auth, users

# telling the Postgres to builds the tables
app.db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to AD's task manager!"}


# DNS (Domain Name System): How does google.com turn into an IP address?
# JSON vs. XML: Why did we choose JSON for our Task Manager?
# RESTful API Principles: This is the "Gold Standard" of how APIs should be organized. You are already building a REST API, but reading the "rules" will make you feel much more confident.
