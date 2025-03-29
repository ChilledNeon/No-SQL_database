# Importing project files
from models import Task, TaskOut, TaskUpdate
from db import collection

# Importing actual
from fastapi import FastAPI, HTTPException, status
from bson.objectid import ObjectId
from bson.errors import InvalidId
from typing import List

app = FastAPI()

# All the "@" are called a decorator. They are needed for defining endpoints 
@app.get("/tasks", response_model=List[TaskOut]) # This defines a get request. The /task defines the URL needed. 
                                                    #Finally, The responce model is the output format that will be received, in this case, it is taskout from the models file
def get_all_tasks():
    tasks = [] # Define a list to hold all the tasks
    for task in collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "task": task["task"],
            "done": task["done"]
        }) # Append the tasks, formated in the TaskOut format as stated before.
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskOut) # The url this time requires the id of the task to get it, with the responce being TaskOut
                                                        # In practice, the task id won't be used by the user, just by the GUI. A GUI then would send it to the database
def get_task(task_id: str):
    try:
        task = collection.find_one({"_id": ObjectId(task_id)}) # First step is to try and find it. Use the try here so we can handle the error properly
    except InvalidId: # Exeption being the id not being found (Invaild)
        raise HTTPException(status_code=400, detail="Invalid task ID format") # If the id isn't there raise a 400 (Bad Request) exception
    
    # The reason this is a 400 exception, not a 404 exception, is because not found is if the id is found, but the data inside of it is not there
        # Here, we are using the 400 because it thinks you mistyped the id, not that it's not there

    # If the ID is in the database
    if task: # Find the task
        return {
            "id": str(task["_id"]),
            "task": task["task"],
            "done": task["done"]
        } # Return it in this output, the TaskOut response format
    else: # If the data isn't in the task, return a 404 error
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED) # all the previous points are the same here, except the 201 created response
                                                # The 201 status is here so that it is different from the standard 200 (ok) status response
                                                    # If it wasn't here, the reponse would be 200
def add_task(task: Task):
    result = collection.insert_one(task.dict()) # Making a variable to be a collection that can be inserted into the database
    return {
        "id": str(result.inserted_id),
        "task": task.task,
        "done": task.done
    }

@app.put("/tasks/{task_id}", response_model=TaskOut) # The Put request has the task url that also needs the task ID. Again this would be handled by my GUI
def update_task(task_id: str, updated_task: TaskUpdate):  # Use TaskUpdate model. It is here to enable a custom model
    try:
        update_data = updated_task.dict(exclude_unset=True)  # Remove None values

        if not update_data: # If no task are available to be updated, then raise the 400 response 
            raise HTTPException(status_code=400, detail="No valid fields to update")

        result = collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        ) # Make the result variable that allows the user to update only one of the elements in the database, thus the need for the custom model
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    if result.matched_count == 0: # Did the database find an updated task? if not, raise the 404 response
        raise HTTPException(status_code=404, detail="Task not found")

    updated_doc = collection.find_one({"_id": ObjectId(task_id)}) # Making a variable such that there is only one in the database
    return {
        "id": str(updated_doc["_id"]),
        "task": updated_doc["task"],
        "done": updated_doc["done"]
    }

@app.delete("/tasks/{task_id}") # URL, needs the task ID
def delete_task(task_id: str):
    result = collection.delete_one({"_id": ObjectId(task_id)}) # Deleting one task based on the task ID
    if result.deleted_count == 1: # If the amount of deleted items is only one (Should not be more than one)
        return {"message": f"Task {task_id} deleted successfully!"} # Will give the standard 200 (Ok) response
    else:
        raise HTTPException(status_code=404, detail="Task not found") # If the one task exsits, but nothing is there, raise the 404 response
    
    # Because of the nature of the deletion, there will be no task returned, Unlike the other requests
