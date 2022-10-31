from fastapi import APIRouter, Depends, Request, Form, status

from sqlalchemy.orm import Session
from database import get_db
import models
from hashing import Hasher
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()



@router.get("/deposits")
def deposits(req: Request):
    return templates.TemplateResponse("deposits.html", {"request": req})


@router.post("/deposits")
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
