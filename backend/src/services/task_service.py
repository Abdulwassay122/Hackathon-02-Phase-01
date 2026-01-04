from typing import List
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.utils.exceptions import TaskNotFoundException

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task: TaskCreate) -> Task:
        db_task_data = task.model_dump()
        db_task = Task(**db_task_data)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def get_task(self, task_id: int, user_id: str) -> Task:
        task = self.session.get(Task, task_id)
        if not task:
            raise TaskNotFoundException(task_id)
        if task.user_id != user_id:
            raise PermissionError("Not authorized to access this task")
        return task

    def get_tasks(self, user_id: str) -> List[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = self.session.exec(statement).all()
        return tasks

    def update_task(self, task_id: int, task_data: TaskUpdate, user_id: str) -> Task:
        task = self.get_task(task_id, user_id)
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int, user_id: str) -> bool:
        task = self.get_task(task_id, user_id)
        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_task_completion(self, task_id: int, user_id: str) -> Task:
        task = self.get_task(task_id, user_id)
        task.completed = not task.completed
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_completed_tasks(self, user_id: str) -> List[Task]:
        """Get all completed tasks for a user"""
        statement = select(Task).where(Task.user_id == user_id, Task.completed == True)
        tasks = self.session.exec(statement).all()
        return tasks

    def get_pending_tasks(self, user_id: str) -> List[Task]:
        """Get all pending tasks for a user"""
        statement = select(Task).where(Task.user_id == user_id, Task.completed == False)
        tasks = self.session.exec(statement).all()
        return tasks