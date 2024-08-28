### Chat
# - `POST /api/chat/settings`: Alter chat settings
# - `POST /api/chat/send`: Send message
# - `POST /api/chat/select/ai`: Select AI
# - `POST /api/chat/select/knowledge_graph`: Select Knowledge Graph
# - `GET /api/chat/history/{sessionId}`: Get chat history for a session
# - `POST /api/chat/history/{sessionId}`: Save chat history for a session


from fastapi import APIRouter

router = APIRouter()


@router.get("/chats")


import ray
from fastapi import FastAPI, HTTPException
from typing import List, Optional
import daft
from datetime import datetime


@app.post("/messages", response_model=str)
async def create_message(message: MessageCreate):
    message_id = ray.get(chat_app.new_message.remote(message))
    return message_id


@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: str, update: MessageUpdate):
    updated_message = ray.get(chat_app.edit_message.remote(message_id, update))
    if updated_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message


@app.delete("/messages/{message_id}", response_model=bool)
async def delete_message(message_id: str):
    deleted = ray.get(chat_app.delete_message.remote(message_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
    return True


@app.get("/messages/{message_id}", response_model=Message)
async def get_message(message_id: str):
    message = ray.get(chat_app.get_message.remote(message_id))
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.get("/messages", response_model=List[Message])
async def get_chat_history():
    return ray.get(chat_app.get_chat_history.remote())


# ChatApp Ray Actor
@ray.remote
class ChatRoom(CustomModel):
    def __init__(self, ):

        # Initialize blank Daft DataFrame with the correct schema
        self.df = daft.from_pyarrow({
            "id": [],
            "C"
            "content": [],
            "role": [],
            "user_id": [],
            "agent_id": [],
            "model_id": [],
            "timestamp": [],
            "version": [],
            "edit_history": []
        })

    def create_message(self, message: MessageCreate) -> str:
        msg = Message(**message.dict())
        self._add_to_dataframe(msg)
        self._check_autosave()
        return msg.id

    def edit_message(self, message_id: str, update: MessageUpdate) -> Optional[Message]:
        for i, row in enumerate(self.df.collect()):
            if row['id'] == message_id:
                updated_msg = Message(**row)
                updated_msg.content = update.content
                updated_msg.version += 1
                updated_msg.edit_history.append({
                    "timestamp": datetime.utcnow(),
                    "edit_note": update.edit_note
                })
                self.df = self.df.update(i, updated_msg.dict())
                self._check_autosave()
                return updated_msg
        return None

    def delete_message(self, message_id: str) -> bool:
        initial_len = len(self.df)
        self.df = self.df.filter(self.df['id'] != message_id)
        if len(self.df) < initial_len:
            self._check_autosave()
            return True
        return False

    def get_message(self, message_id: str) -> Optional[Message]:
        for row in self.df.collect():
            if row['id'] == message_id:
                return Message(**row)
        return None

    def get_chat_history(self) -> List[Message]:
        return [Message(**row) for row in self.df.collect()]

    def _add_to_dataframe(self, message: Message):
        new_row = daft.from_pydict(message.dict())
        self.df = self.df.concat(new_row)

    def save(self):
        uc_client = get_uc()

        table = uc_client.

    # Other methods (save_to_firestore, load_from_firestore, etc.) remain the same
    # ...


# Initialize Ray and create ChatApp instance
ray.init()
chat_app = ChatApp.remote("path/to/firebase_credentials.json")

# FastAPI app
app = FastAPI()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Explanation:

1. Pydantic Models:
   - We define Pydantic models (MessageBase, MessageCreate, MessageUpdate, Message) to represent our data structure.
   - These models ensure type safety and provide automatic validation.

2. Daft DataFrame:
   - In the ChatApp __init__ method, we initialize a blank Daft DataFrame with the correct schema based on our Message model.

3. ChatApp Methods:
   - We've updated the ChatApp methods to work with the Pydantic models and Daft DataFrame.
   - Operations like adding, updating, and deleting messages now interact directly with the Daft DataFrame.

4. FastAPI Routes:
   - We've added FastAPI routes for creating, updating, deleting, and retrieving messages.
   - These routes interact with the ChatApp Ray actor, allowing REST API access to our chat functionality.

5. Error Handling:
   - We use HTTPException to handle cases where messages are not found.

Usage:
1. Run the FastAPI server: `python your_script.py`
2. Interact with the API using HTTP requests:
   - POST /messages: Create a new message
   - PUT /messages/{message_id}: Update an existing message
   - DELETE /messages/{message_id}: Delete a message
   - GET /messages/{message_id}: Retrieve a specific message
   - GET /messages: Get the entire chat history

This setup provides a robust, type-safe API for interacting with our ChatApp, 
combining the distributed computing power of Ray, the data processing capabilities of Daft, 
and the API development simplicity of FastAPI.
"""
