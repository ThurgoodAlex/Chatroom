from fastapi import APIRouter, Depends
from backend import database as db
from backend.auth import auth_get_current_user

from backend.schema import(
  UserInDB, ChatCollection, UserResponse, UserCollection, UserUpdate
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(Session = Depends(db.get_session)):
    """Getting a collection of users sorted by ID"""

    def sort_key(user): return user.id
    users = db.get_all_users(Session)

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key),
    )

@users_router.get("/me", response_model=UserResponse)
def get_current_user(user: UserInDB = Depends(auth_get_current_user)):
    """Get current user."""
    return UserResponse(user=user)

@users_router.put("/me", response_model=UserResponse, status_code=200)
def update_user(user_update:UserUpdate, current_user: UserInDB = Depends(auth_get_current_user), Session = Depends(db.get_session)):
    """Updates the current users username and or email"""
    user = db.update_user(Session, current_user, user_update )
    print(user)
    return UserResponse(user=user)

@users_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int,Session = Depends(db.get_session)):
    """Get a user by a given id"""
    return UserResponse(user=db.get_user_by_id(Session,user_id))

@users_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_users_chats(user_id: int,Session = Depends(db.get_session)):
    """Get chats based on a giver id"""
    user = db.get_user_by_id(Session, user_id)
    if user:
        chats = user.chats
    def sort_key(chat): return getattr(chat, "name")
    response =  ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key)
    )
    return response