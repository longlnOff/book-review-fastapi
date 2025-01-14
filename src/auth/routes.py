from fastapi import APIRouter, status, HTTPException, Depends
from src.auth.schemas import UserCreateModel, UserModel
from src.auth.service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

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
