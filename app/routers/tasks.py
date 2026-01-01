from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.security import OAuth2PasswordRequestForm
from enum import Enum

# custom imports
from app.models import TaskResponse, TaskCreate, TaskStatus, TaskUpdate, SortOrder
from app.db_models import DBTask, DBUser
from app.database import get_db
from app.dependencies import get_current_user
router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ---Create---
@router.post("/", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    # 1. Convert Pydantic model to SQLAlchemy model
    new_db_task = DBTask(**task_in.model_dump(), owner_id=current_user.id)

    # 2. Save to the database
    db.add(new_db_task)
    db.commit()
    # 3. Refresh to get the generated ID and Timestamp
    db.refresh(new_db_task)

    return new_db_task


# ---Read---
@router.get("/{task_id}", response_model=TaskResponse)
def read_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[int] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    sort_order: Optional[SortOrder] = SortOrder.ascending,
    db: Session = Depends(get_db),
    current_user: OAuth2PasswordRequestForm = Depends(get_current_user),
):
    query = db.query(DBTask).filter(DBTask.owner_id == current_user.id)
    if status:
        query = query.filter(DBTask.status == status)
    if priority:
        query = query.filter(DBTask.priority == priority)

    if sort_order == SortOrder.ascending:
        query = query.order_by(DBTask.id)
    else:
        query = query.order_by(desc(DBTask.id))
    tasks = query.offset(skip).limit(limit).all()

    return tasks


# ---update---
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: OAuth2PasswordRequestForm = Depends(get_current_user),
):
    task = (
        db.query(DBTask)
        .filter(DBTask.id == task_id, DBTask.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if isinstance(value, Enum):
            setattr(task, key, value.value)
        else:
            setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


# ---Delete---
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: OAuth2PasswordRequestForm = Depends(get_current_user),
):
    task_to_delete = (
        db.query(DBTask)
        .filter(DBTask.id == task_id, DBTask.owner_id == current_user.id)
        .first()
    )
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_to_delete)
    db.commit()
    return {"message": "Task Deleted!"}
