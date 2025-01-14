from fastapi import APIRouter, status, HTTPException, Depends
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse



router = APIRouter()

user_service = UserService()

@router.post(
        "/signup",
        response_model=UserModel,
        status_code=status.HTTP_201_CREATED        
)
async def create_user_Account(user_data: UserCreateModel, 
                              session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")

    user = await user_service.create_user(user_data, session)
    return user

@router.post(
        "/login",
        response_model=UserModel,
        status_code=status.HTTP_200_OK
)
async def login_users(user_data: UserLoginModel, 
                      session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    is_password_valid = verify_password(password, user.password_hash)
    if not is_password_valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password")

    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid)
        }
    )

    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid)
        },
        refresh=True,
        expiry=timedelta(hours=24)
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_uid": str(user.uid),
                "email": user.email
            }
        }
    )