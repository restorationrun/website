from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import datetime
import sqlite3
import hashlib
from dotenv import load_dotenv
import os

con = sqlite3.connect("data.db")

# https://medium.com/@chodvadiyasaurabh/integrating-stripe-payment-gateway-with-fastapi-a-comprehensive-guide-8fe4540b5a4

metadata_tags = [
    {
        "name": "web",
        "description": "Webpages and related APIs.",
    },
    {
        "name": "db",
        "description": "Database Utilities.",
    },
]

load_dotenv()
current_year = str(datetime.datetime.today()).split("-")[0]

app = FastAPI(
    title="Restoration Run",
    version="2024.06.30",
    openapi_tags=metadata_tags,
)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")


def hash_me(s:str) -> str:
    '''Returns the SHA1 hash of the string'''
    return hashlib.sha1(s.encode()).hexdigest()


@app.get("/", response_class=HTMLResponse, tags=["web"])
def website(request: Request):
    program_template = "index.html"
    return templates.TemplateResponse(
        program_template, {"request": request, "year": current_year}
    )


@app.get("/race-course", response_class=HTMLResponse, tags=["web"])
def map(request: Request):
    program_template = "map.html"
    return templates.TemplateResponse(
        program_template, {"request": request, "year": current_year}
    )


@app.post("/register", tags=["web"])  # , response_class=HTMLResponse, tags=["web"])
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    zip: str = Form(...),
    size: str = Form(...),
    consent_publish: str = Form(...),
    consent_marketing: str = Form(...),
):
    # Convert form checkboxes to 1 or 0
    if consent_publish == "on":
        consent_publish = 1
    else:
        consent_publish = 0

    if consent_marketing == "on":
        consent_marketing = 1
    else:
        consent_marketing = 0

    # Get the registration details
    data = {
        "id": hash_me(email),
        "name": name,
        "email": email,
        "password": hash_me(password),
        "phone": phone,
        "zip": zip,
        "size": size,
        "consent_publish": consent_publish,
        "consent_marketing": consent_marketing,
    }

    # upsert the data to the database
    return data
    # program_template = "register.html"
    # return templates.TemplateResponse(
    #    program_template, {"request": request, "year": current_year}
    # )


@app.get("/what-is-the-restoration", response_class=HTMLResponse, tags=["web"])
def restoration(request: Request):
    program_template = "restoration.html"
    return templates.TemplateResponse(
        program_template, {"request": request, "year": current_year}
    )


# Run uvicorn if it's the dev machine
if "DEV" in os.environ:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
