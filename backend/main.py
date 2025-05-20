from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  HTMLResponse
from .chatbot import get_response
from fastapi.templating import Jinja2Templates  

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")
    bot_response = get_response(user_message)
    return {"response": bot_response}




@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )