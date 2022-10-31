from fastapi import APIRouter, Depends, Request, Form, status

from sqlalchemy.orm import Session
from database import get_db
import models
from hashing import Hasher
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    sign_up = db.query(models.users).all()
    return templates.TemplateResponse("base.html", {"request": req})


# @app.get("/")
# async def home_login(req: Request, db: Session = Depends(get_db)):
#     sign_up = db.query(models.signup).all()
#     return templates.TemplateResponse("login.html")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
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
