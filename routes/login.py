from fastapi import APIRouter, Depends, Request, Form, status, responses

from sqlalchemy.orm import Session
from database import get_db
import models
from hashing import Hasher
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()



@router.get("/login")
def login(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})


@router.post("/login")
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
            # return templates.TemplateResponse('deposits.html', {"request": req})
            return responses.RedirectResponse(
                "/deposits", status_code=status.HTTP_302_FOUND
            )
        else:
            return "wrong password"

    # return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
