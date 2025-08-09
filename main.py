from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
import string
import hashlib

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for input
class TextInput(BaseModel):
    text: str

# Generate random token
def generate_token(length: int = 16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Route: Homepage with HTML
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "Jaya Narayana"})

# Route: Generate Token
@app.get("/generate-token")
async def generate_token_api():
    return {"token": generate_token()}

# Route: Generate checksum of input text
@app.post("/generate-checksum")
async def generate_checksum(data: TextInput):
    checksum = hashlib.sha256(data.text.encode()).hexdigest()
    return {"checksum": checksum}
