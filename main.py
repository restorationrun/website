from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime
#from dotenv import load_dotenv, find_dotenv
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2 import service_account

# https://medium.com/@chodvadiyasaurabh/integrating-stripe-payment-gateway-with-fastapi-a-comprehensive-guide-8fe4540b5a4

metadata_tags = [
    {
        "name": "web",
        "description": "Webpages and related APIs.",
    },
]

app = FastAPI(
    title="Restoration Run",
    version="2024.06.30",
    openapi_tags=metadata_tags,
)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/images", StaticFiles(directory="images"), name="images")

templates = Jinja2Templates(directory="templates")

current_year = str(datetime.datetime.today()).split("-")[0]

@app.get("/", response_class=HTMLResponse, tags=["web"])
def website(request: Request):
    program_template = "index.html"
    return templates.TemplateResponse(program_template, {"request": request, "year": current_year})

'''
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''