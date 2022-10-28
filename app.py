from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    sign_up = db.query(models.signup).all()
    return templates.TemplateResponse("base.html", {"request": req, "todo_list": sign_up})


@app.get("/")
async def home_login(req: Request, db: Session = Depends(get_db)):
    sign_up = db.query(models.signup).all()
    return templates.TemplateResponse("login.html")


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(req: Request,
           first_name: str = Form(...),
           last_name: str = Form(...),
           email: str = Form(...),
           contact: str = Form(...),
           password: str = Form(...), db: Session = Depends(get_db)):
    new_signup = models.signup(first_name=first_name,
                               last_name=last_name,
                               email=email,
                               contact=contact,
                               password=password)
    db.add(new_signup)
    db.commit()
    db.close()
    url = app.url_path_for("home")

    # return 'success'
    #
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)



@app.get("/login")
def login():
    return templates.TemplateResponse('login.html')

@app.post("/login")
def login(req: Request,
          email: str = Form(...),
          password: str = Form(...), db: Session = Depends(get_db)):
    new_signup = models.signup(email=email,
                               password=password)
    db.add(new_signup)
    db.commit()
    # db.close()
    url = app.url_path_for("home_login")

    return templates.TemplateResponse('login.html')

    # return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

#
# @app.get("/update/{todo_id}")
# def add(req: Request, todo_id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     todo.complete = not todo.complete
#     db.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
#
#
# @app.get("/delete/{todo_id}")
# def add(req: Request, todo_id: int, db: Session = Depends(get_db)):
#     todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
#     db.delete(todo)
#     db.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
