from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn, secrets, os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("CYBEL_USER", "cybel")
PASSWORD = os.getenv("CYBEL_PASS", "yourpassword123")

security = HTTPBasic()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def cybel_brain(query: str):
    return f"CYBEL Response to: {query}"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

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

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)