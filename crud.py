from sqlalchemy.orm import Session
import models, schemas

def get_todos(db: Session):
    return db.query(models.Todo).all()

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoCreate):
    db_todo = get_todos(db, todo_id)
    if not db_todo:
        return None
    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db.commit()
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo

    