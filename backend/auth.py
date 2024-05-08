import os
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError
from typing import Annotated
from sqlmodel import Session, SQLModel, select
from jose import ExpiredSignatureError, JWTError, jwt
from backend import database as db
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from backend.schema import(
    UserInDB, UserResponse
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_key = str(os.environ.get("JWT_KEY"))
jwt_alg = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
access_token_duration = 3600 


class DuplicateUserRegistration(HTTPException):
    status_code = 409
    default_detail = "Entity already exists."
    def __init__(self, entity_name: str, entity_field: str, entity_value: str):
        self.entity_name = entity_name
        self.entity_field = entity_field
        self.entity_value = entity_value
        detail = f"{entity_name} with {entity_field} '{entity_value}' already exists."
        super().__init__(status_code=self.status_code, detail=detail)

class AuthException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=401,
            detail={
                "error": error,
                "error_description": description,
            },
        )

class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid username or password",
        )

class InvalidToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid access token",
        )


class ExpiredToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="expired access token",
        )


class UserRegistration(BaseModel):
    """Request model to register new user."""
    username: str
    email: str
    password: str

class AccessToken(BaseModel):
    """Response model for an access token"""
    access_token: str
    token_type: str
    expires_in: int


class Claims(BaseModel):
    """Access token claims (aka payload)."""

    sub: str  # id of user
    exp: int  # unix timestamp


def auth_get_current_user(session = Depends(db.get_session),token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = decode_access_token(session, token)

    return user


@auth_router.post("/registration", response_model=UserResponse, status_code=201)
def register_new_user(newUser: UserRegistration, session: Annotated[Session, Depends(db.get_session)]) ->UserResponse:
    """Register a new user"""
    hashed_password = pwd_context.hash(newUser.password)
    # print(newUser)
    if check_username(newUser, session):
        raise DuplicateUserRegistration("User", "username", newUser.username)
    elif check_email(newUser, session):
        raise DuplicateUserRegistration("User", "email", newUser.email)
    else:
        user = UserInDB(
            **newUser.model_dump(),
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(user = user)
    
def check_username(newUser, session):
    result = session.exec(select(UserInDB.username).where(UserInDB.username == newUser.username))
    return result.first() is not None
   
def check_email(newUser, session):
    result = session.exec(select(UserInDB.email).where(UserInDB.email == newUser.email))
    return result.first() is not None



@auth_router.post("/token", response_model=AccessToken, status_code=200)
def get_access_token(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session),
    
):
    """Get access token for user."""

    user = get_authenticated_user(session, form)
    return build_access_token(user)


def get_authenticated_user(session: Session,form: OAuth2PasswordRequestForm,) -> UserInDB:
    user = session.exec(select(UserInDB).where(UserInDB.username == form.username)).first()
    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()
    return user



def build_access_token(user: UserInDB) -> AccessToken:
    """Building access token for user"""
    expiration = int(datetime.now(timezone.utc).timestamp()) + access_token_duration
    claims = Claims(sub=str(user.id), exp=expiration)
    access_token = jwt.encode(claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )



def decode_access_token(session: Session, token : str) -> UserInDB:
    """decoding acess token for user"""
    try:
        claims_dict = jwt.decode(token, key = jwt_key, algorithms=[jwt_alg])
        claims = Claims(**claims_dict)
        user_id =claims.sub
        user = session.get(UserInDB, user_id)

        if user is None:
            raise InvalidToken()

      
        return user
    
    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        raise InvalidToken()
    except ValidationError():
        raise InvalidToken()