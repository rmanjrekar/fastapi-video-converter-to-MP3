from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.dependencies import get_db
from models.users import User
from services.user_service import get_current_user, verify_password, get_token, pwd_context
from schemas.users import LoginRequest, UserCreate, UserResponse, LoginResponse, UserDelete

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login_for_access_token(request: LoginRequest, db: Session = Depends(get_db)):
    email = request.email
    password = request.password

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return get_token(user.email)


@router.post("/users", response_model=UserResponse)
def create_user(request: UserCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    body = request
    searched_user = db.query(User).filter(User.email == body.email).first()
    if searched_user:
        raise HTTPException(status_code=409, detail="User already exists")
    else:
        hashed_password = pwd_context.hash(body.password)
        new_user = User(email=body.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    searched_user = db.query(User).filter(User.id == user_id).first()

    if searched_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return searched_user


@router.delete("/users")
async def delete_user(request: UserDelete, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    body = request
    searched_user = db.query(User).filter(User.id == body.id).first()

    if searched_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(searched_user)
    db.commit()

    return {"detail": f"User '{searched_user.email}' deleted successfully"}


@router.get("/health")
def health():
    return {"errors" : None}
