from fastapi import FastAPI, Depends, Request, Form, status, HTTPException
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from database import get_db
from routes import signup, login, deposits, transactions, balance


models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(deposits.router)
app.include_router(transactions.router)
app.include_router(balance.router)
# @app.get("/")
# async def home(req: Request, db: Session = Depends(get_db)):
#     sign_up = db.query(models.users).all()
#     return templates.TemplateResponse("base.html", {"request": req})

