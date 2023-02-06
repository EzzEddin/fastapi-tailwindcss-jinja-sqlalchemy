from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from models import Todo, session


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    todos = session.query(Todo).all()
    context = {
        "request": request,
        "todos": todos,
    }
    return templates.TemplateResponse("home.html", context)

@app.get("/create")
async def create_todo(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("create.html", context)

@app.post("/create")
async def create_todo(
    text: str = Form(),
    is_complete: bool = Form(False)
    ):
    todo = Todo(text=text, is_done=is_complete)
    session.add(todo)
    session.commit()
    return RedirectResponse(
        url=app.url_path_for("home"),
        status_code=302
        )

@app.post("/update/{id}")
async def update_todo(
    id: int,
    new_text: str = Form(""),
    is_complete: bool = Form(False)
    ):
    todo = session.query(Todo).filter(Todo.id==id).first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    session.add(todo)
    session.commit()
    return RedirectResponse(
        url=app.url_path_for("home"),
        status_code=302
        )

@app.get("/update/{id}")
async def update_todo(request: Request, id: int):
    todo_instance = session.query(Todo).filter(Todo.id==id).first()
    context = {"request": request, "todo_instance": todo_instance}
    return templates.TemplateResponse("update.html", context)

@app.post("/delete/{id}")
async def delete_todo(request: Request, id: int):
    todo = session.query(Todo).filter(Todo.id==id).first()
    session.delete(todo)
    session.commit()
    return RedirectResponse(
        url=app.url_path_for("home"),
        status_code=302
        )

@app.get("/delete/{id}")
async def delete_todo(request: Request, id: int):
    todo = session.query(Todo).filter(Todo.id==id).first()
    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("delete.html", context)