from pydantic import BaseModel, Field # Field allows for constraints on the model
from typing import Optional # Makes the field optional to add

class Task(BaseModel): # Adds a full task
    task: str = Field(..., min_length=1, max_length=100, description="Name of the task") # adds a "Task" with constraints of word length of 1-100
    done: bool = False # Wouldn't be adding a task if it were done

class TaskOut(BaseModel): # Returns a full task
    id: str  # This will be the string version of MongoDB's _id
    task: str
    done: bool

class TaskUpdate(BaseModel): #Updates a task
    task: Optional[str] = None # The optional part here implies that you don't need both to update the full task
    done: Optional[bool] = None