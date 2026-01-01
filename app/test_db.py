from database import SessionLocal
from db_models import DBTask

def test_connection():
    # 1. Create a new session (Open the door to the DB)
    db = SessionLocal()

    try:
        print("Connecting to the database...")
        # 2. Query the database for all tasks
        tasks = db.query(DBTask).all()

        print(f"Found {len(tasks)} tasks in the database:")
        for task in tasks:
            print(f"ID: {task.id} | Title: {task.title} | Priority: {task.priority}")

    except Exception as e:
        print(f"Error: Could not connect. {e}")
    finally:
        # 3. Always close the session
        db.close()

if __name__ == "__main__":
    test_connection()