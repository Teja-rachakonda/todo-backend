from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    completed: bool = False
    
class TodoRead(TodoCreate):
    id: int
    
    class config:
        orm_mode = True
        
        