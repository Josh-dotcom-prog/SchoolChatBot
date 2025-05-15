from fastapi import FastAPI, Request, HTTPException
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

app = FastAPI()

chatbot = ChatBot("StudentHelpDesk")
trainer = ListTrainer(chatbot)

# Load training data
with open("data/training_data.json") as f:
    qa_pairs = json.load(f)

for pair in qa_pairs:
    trainer.train([pair["question"], pair["answer"]])

def get_response(message):
    return str(chatbot.get_response(message))

@app.post("/chat")
async def chat(request: Request):
    try:
        # Read raw body
        body_bytes = await request.body()

        if not body_bytes:
            raise HTTPException(status_code=400, detail="Empty request body")

        body = json.loads(body_bytes)
        user_message = body.get("message")

        if not user_message:
            raise HTTPException(status_code=422, detail="Missing 'message' field")

        bot_response = get_response(user_message)
        return {"response": bot_response}

    except json.JSONDecodeError as e:
        print("Invalid JSON format:", e)
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        print("Unexpected error:", e)
        raise HTTPException(status_code=500, detail="Server error")
