from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    contact = Column(String(100))
    password = Column(String(100))

    user_deposits = relationship("deposits", back_populates='customer')


class deposits(Base):
    __tablename__ = 'deposits'

    id = Column(Integer, primary_key=True)
    amount = Column(String(100))
    # user_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    customer = relationship("users", back_populates='user_deposits')

#
# @router.get("/login")
# def login(request: Request, msg:str=None):
#     return templates.TemplateResponse("login.html", {"request": request , "msg" : msg})
#
#
# @router.post("/login")
# async def login(response: Response, request: Request, db: Session = Depends(get_db)):
#     form = await request.form()
#     email = form.get("email")
#     password = form.get("password")
#     errors = []
#     if not email:
#         errors.append("Please Enter valid Email")
#     if not password:
#         errors.append("Password enter password")
#     if len(errors) > 0:
#         return templates.TemplateResponse(
#             "login.html", {"request": request, "errors": errors}
#         )
#     try:
#         user = db.query(Users).filter(Users.email == email).first()
#         if user is None:
#             errors.append("Email does not exists")
#             return templates.TemplateResponse(
#                 "login.html", {"request": request, "errors": errors}
#             )
#         else:
#             if Hasher.verify_password(password, user.password):
#                 data = {"sub": email}
#                 jwt_token = jwt.encode(
#                     data, setting.SECRET_KEY, algorithm=setting.ALGORITHM
#                 )
#                 # if we redirect response in below way, it will not set the cookie
#                 # return responses.RedirectResponse("/?msg=Login Successfull", status_code=status.HTTP_302_FOUND)
#                 msg = "Login Successful"
#                 response = templates.TemplateResponse(
#                     "flat_homepage.html", {"request": request, "msg": msg}
#                 )
#                 response.set_cookie(
#                     key="access_token", value=f"Bearer {jwt_token}", httponly=True
#                 )
#                 return response
#             else:
#                 errors.append("Invalid Password")
#                 return templates.TemplateResponse(
#                     "login.html", {"request": request, "errors": errors}
#                 )
#     except:
#         errors.append("Something Wrong while authentication or storing tokens!")
#         return templates.TemplateResponse(
#             "login.html", {"request": request, "errors": errors}
#         )
