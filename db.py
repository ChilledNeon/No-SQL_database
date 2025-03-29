from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") # Establishes connection to the MongoDB database on the default port
db = client["todo_db"] # Updates the database "todo_db"
                            #If it doesn't exsist already, the client will automatically create and save it once you write something to it
collection = db["tasks"] # Collection is similar to SQL 
                            #Instead of saving as rows, it is saved as Json
