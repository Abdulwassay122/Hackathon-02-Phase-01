"""
Database seeding script for initial data
"""
from sqlmodel import Session, select
from backend.src.database.connection import engine, create_db_and_tables
from backend.src.models.task import Task, TaskCreate

def seed_database():
    """
    Seed the database with initial data
    """
    print("Seeding database...")

    # Create tables
    create_db_and_tables()

    # Create initial tasks for demo purposes
    with Session(engine) as session:
        # Check if we already have tasks
        existing_tasks = session.exec(select(Task)).all()
        if len(existing_tasks) > 0:
            print("Database already seeded, skipping...")
            return

        # Create sample tasks
        sample_tasks_data = [
            {
                "title": "Sample Task 1",
                "description": "This is a sample task for demonstration",
                "completed": False,
                "user_id": 1
            },
            {
                "title": "Sample Task 2",
                "description": "Another sample task",
                "completed": True,
                "user_id": 1
            },
            {
                "title": "Learn FastAPI",
                "description": "Complete the tutorial and build a project",
                "completed": False,
                "user_id": 2
            }
        ]

        for task_data in sample_tasks_data:
            task = Task(**task_data)
            session.add(task)

        session.commit()
        print(f"Seeded {len(sample_tasks_data)} tasks successfully!")

if __name__ == "__main__":
    seed_database()