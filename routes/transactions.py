
from fastapi import APIRouter, Depends, Request, Form, status

from sqlalchemy.orm import Session
from database import get_db
import models
from hashing import Hasher
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()




@router.get("/transactions")
def transactions(req: Request):
    return templates.TemplateResponse("transactions.html", {"request": req})


@router.post("/transactions")
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