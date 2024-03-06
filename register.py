from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import uvicorn
import logging

app = FastAPI()


templates = Jinja2Templates(directory="templates")


client = MongoClient(
    "mongodb+srv://shinchan:nightingale@cluster0.y0gzl8x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["shinchan"]
collection = db["users"]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(request: Request):
    form = await request.form()
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")

    user_data = {"username": username, "email": email, "password": password}
    collection.insert_one(user_data)
    logging.info("My test completed .... ")
    return templates.TemplateResponse("register.html", {"request": request})
    # return result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
