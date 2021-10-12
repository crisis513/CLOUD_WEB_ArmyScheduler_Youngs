from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
from dotenv import load_dotenv
load_dotenv() 

import api.sample.urls as service_1
import api.users.urls as users
import api.works.urls as works

app = FastAPI()

app.include_router(service_1.router, prefix="/api/v1/service_1")
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(works.router, prefix="/api/v1/works")

# Mounting default Vue files after running npm run build 
app.mount("/dist", StaticFiles(directory="dist/"), name="dist")
app.mount("/css", StaticFiles(directory="dist/css"), name="css")
app.mount("/img", StaticFiles(directory="dist/img"), name="img")
app.mount("/js", StaticFiles(directory="dist/js"), name="js")
templates = Jinja2Templates(directory="dist")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})