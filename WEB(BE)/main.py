from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.jwt_bearer import JWTBearer

import os
from dotenv import load_dotenv
load_dotenv() 

import api.users.urls as users
import api.works.urls as works
import api.events.urls as events
import api.admin as admin
import api.schedule.urls as schedule

app = FastAPI()

token_listener = JWTBearer()

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(works.router, prefix="/api/v1/works")
app.include_router(events.router, prefix="/api/v1/events")
app.include_router(admin.router, prefix="/jwt/admin")
app.include_router(schedule.router, prefix="/api/v1/schedule")

# Mounting default Vue files after running npm run build 
app.mount("/dist", StaticFiles(directory="dist/"), name="dist")
app.mount("/css", StaticFiles(directory="dist/css"), name="css")
app.mount("/img", StaticFiles(directory="dist/img"), name="img")
app.mount("/js", StaticFiles(directory="dist/js"), name="js")
templates = Jinja2Templates(directory="dist")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
