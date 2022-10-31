from _curses import flash

from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import hashing
from database import SessionLocal, engine
import models
from hashing import Hasher

#
# print(Hasher.get_password_hash('satyam'))
# print(Hasher.verify_password('satyam',Hasher.get_password_hash('satyam')))


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
    sign_up = db.query(models.users).all()
    return templates.TemplateResponse("base.html", {"request": req})


# @app.get("/")
# async def home_login(req: Request, db: Session = Depends(get_db)):
#     sign_up = db.query(models.signup).all()
#     return templates.TemplateResponse("login.html")


@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(req: Request,
                 first_name: str = Form(...),
                 last_name: str = Form(...),
                 email: str = Form(...),
                 contact: str = Form(...),
                 password: str = Form(...), db: Session = Depends(get_db)):
    form = await req.form()
    email = form.get("email")
    password = Hasher.get_password_hash(form.get("password"))
    errors = []
    # if not email:
    #     errors.append('Enter a valid email')
    # if not password:
    #     errors.append("Enter valid password")
    # if len(errors) > 0:
    #     return templates.TemplateResponse(
    #         'base.html', {"request": req, "errors": errors}
    #     )

    # try:
    user = db.query(models.users).filter(models.users.email == email).first()

    if user is None:

        new_signup = models.users(first_name=first_name,
                                  last_name=last_name,
                                  email=email,
                                  contact=contact,
                                  password=password)
        db.add(new_signup)
        db.commit()
        db.close()
        # url = app.url_path_for("home")
        return templates.TemplateResponse("login.html", {"request": req})
        # return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


    else:
        # print("error hai")
        # errors.append("Email already exists")
        return "Email already exists"

        # return templates.TemplateResponse(
        #     'login.html'
        # )
        # raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)

    # except:
    #     errors.append("Something Wrong while authentication or storing tokens!")
    #     print("except main")
    #     return templates.TemplateResponse(
    #         "base.html", {"request": req, "errors": errors}
    #     )

    # return 'success'
    #


# @app.get("/login")
# def login():
#     return templates.TemplateResponse('login.html')

@app.get("/login")
def login(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})


@app.post("/login")
async def login(req: Request,
                email: str = Form(...),
                password: str = Form(...),
                db: Session = Depends(get_db)):
    form = await req.form()

    email = form.get("email")
    password = form.get("password")
    # print(email, password)
    user = db.query(models.users).filter(models.users.email == email).first()

    # print(user.password)

    if user is None:
        return "Wrong Credentials"

    else:
        auth = Hasher.verify_password(password, user.password)
        if auth:

            # return "success"
            return templates.TemplateResponse('deposits.html', {"request": req})
        else:
            return "wrong password"

    # return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/deposits")
def deposits(req: Request):
    return templates.TemplateResponse("deposits.html", {"request": req})


@app.post("/deposits")
async def deposits(req: Request,
                   email: str = Form(...),
                   amount: str = Form(...),
                   db: Session = Depends(get_db)):
    form = await req.form()
    email = form.get("email")
    amount = form.get("amount")
    print(email, amount)

    user = db.query(models.users).filter(models.users.email == email).first()
    print(user)
    if user is None:
        return "invalid user"
    else:
        user_deposit = db.query(models.deposits).filter(models.deposits.user_id == user.id).first()

        if user_deposit:
            print(user_deposit.amount, amount)
            user_deposit.amount = int(user_deposit.amount) + int(amount)
        else:
            new_deposit = models.deposits(amount=amount,
                                          user_id=user.id)
            db.add(new_deposit)
            # print(new_deposit)

        db.commit()
        db.close()
        return templates.TemplateResponse("deposits.html", {"request": req})


@app.get("/transactions")
def transactions(req: Request):
    return templates.TemplateResponse("transactions.html", {"request": req})


@app.post("/transactions")
async def transactions(req: Request,
                       sender: str = Form(...),
                       receiver: str = Form(...),
                       amount: str = Form(...),
                       db: Session = Depends(get_db)):
    form = await req.form()
    sender = form.get("sender")
    receiver = form.get("receiver")
    amount = form.get("amount")

    sender_user = db.query(models.users).filter(models.users.email == sender).first()
    if sender_user is None:
        return "sender is invalid"

    receiver_user = db.query(models.users).filter(models.users.email == receiver).first()
    if receiver_user is None:
        return "receiver is invalid"

    sender_deposit = db.query(models.deposits).filter(models.deposits.user_id == sender_user.id).first()

    receiver_deposit = db.query(models.deposits).filter(models.deposits.user_id == receiver_user.id).first()

    if sender_deposit is None:
        return "sender has no deposits"
    else:
        if receiver_deposit is None:
            new_receiver_deposit = models.deposits(amount=amount,
                                                   user_id=receiver_user.id)
            if int(amount) > int(sender_deposit.amount):
                return "sender doesn't have that much deposit"
            else:
                sender_deposit.amount = int(sender_deposit.amount) - int(amount)

            db.add(new_receiver_deposit)
            db.commit()
            db.close()
            return "success"
        else:
            if int(amount) > int(sender_deposit.amount):
                return "sender doesn't have that much deposit"
            else:
                sender_deposit.amount = int(sender_deposit.amount) - int(amount)

            receiver_deposit.amount = int(receiver_deposit.amount) + int(amount)
            db.commit()
            db.close()
            return "success"

    return templates.TemplateResponse("transactions.html", {"request": req})


@app.get("/balance")
def balance(req: Request):
    return templates.TemplateResponse("balance.html", {"request": req})


@app.post("/balance")
async def balance(req: Request,
                  email: str = Form(...),
                  db: Session = Depends(get_db)):
    form = await req.form()
    email = form.get("email")

    user = db.query(models.users).filter(models.users.email == email).first()
    print(user)
    if user is None:
        return "invalid user"
    else:
        user_deposit = db.query(models.deposits).filter(models.deposits.user_id == user.id).first()

        if user_deposit:
            balance = []
            balance.append(user_deposit.amount)
            return templates.TemplateResponse("balance.html", {"request": req, "balance": balance})
        else:
            balance = []
            balance.append(0)
            return templates.TemplateResponse("balance.html", {"request": req, "balance": balance})


    # return templates.TemplateResponse("balance.html", {"request": req, "balance": balance})

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
