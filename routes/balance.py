
from fastapi import APIRouter, Depends, Request, Form, status

from sqlalchemy.orm import Session
from database import get_db
import models
from hashing import Hasher
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()



@router.get("/balance")
def balance(req: Request):
    return templates.TemplateResponse("balance.html", {"request": req})


@router.post("/balance")
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
