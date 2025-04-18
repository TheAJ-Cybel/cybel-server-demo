from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {{ "request": request }})

@app.post("/ask", response_class=JSONResponse)
async def ask(request: Request, query: str = Form(...)):
    try:
        current_time = "Friday, April 18, 2025 at 02:12"
        messages = [
            {{
                "role": "system",
                "content": (
                    "You are CYBEL, a brilliant, kind, witty, and deeply helpful AI assistant. "
                    "You speak fluently and naturally, like a human. You understand context and show empathy. "
                    "Today is " + current_time + ". "
                    "Provide helpful and informative answers. When relevant, you may show curiosity, humor, or philosophical depth."
                )
            }},
            {{
                "role": "user",
                "content": query
            }}
        ]
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.85,
            top_p=0.95
        )
        reply = completion.choices[0].message["content"]
        return {{ "response": reply }}

    except Exception as e:
        return {{ "response": f"[Error]: {{str(e)}}" }}