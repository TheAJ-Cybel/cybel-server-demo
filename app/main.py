from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai
import secrets
import os

load_dotenv()

# Secure login credentials
USERNAME = os.getenv("CYBEL_USER", "cybel")
PASSWORD = os.getenv("CYBEL_PASS", "yourpassword123")

# OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Authentication dependency
security = HTTPBasic()
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# Smart brain function using GPT-4
def cybel_brain(query: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are CYBEL, a helpful AI assistant with expert knowledge."},
                {"role": "user", "content": query}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[Error]: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request, auth: bool = Depends(authenticate)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_class=JSONResponse)
async def ask_post(query: str = Form(...), auth: bool = Depends(authenticate)):
    response = cybel_brain(query)
    return {"response": response}

@app.get("/ask", response_class=JSONResponse)
async def ask_get(query: str, auth: bool = Depends(authenticate)):
    response = cybel_brain(query)
    return {"response": response}