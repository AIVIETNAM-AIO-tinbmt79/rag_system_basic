from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from rag_system_basic.rag_system.app.database.session import get_db

from rag_system_basic.rag_system.app.database.crud import (
    create_user,
    get_user_by_email
)

from rag_system_basic.rag_system.app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from rag_system_basic.rag_system.app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        request.email
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hashed_pw = hash_password(
        request.password
    )

    user = create_user(
        db=db,
        username=request.username,
        email=request.email,
        hashed_password=hashed_pw
    )

    return {
        "message": "User created successfully",
        "user_id": user.id
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = get_user_by_email(
        db,
        request.email
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(
        request.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        {
            "sub": user.email
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )