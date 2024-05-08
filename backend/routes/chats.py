
from fastapi import APIRouter, Depends, Query
from backend import database as db
from backend.auth import auth_get_current_user

from backend.schema import (
     ChatCollection,ChatResponse, ChatUpdate, MessageCollection, UserCollection,
    MessageInDB,CreateMessage, UserInDB, MessageResponse,  UsersAndMessagesAndChats,
    ChatMetaData, 
    
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("", response_model=ChatCollection)
def get_all_chats(Session = Depends(db.get_session)):
    """Getting all the chats sorted by name"""
    def sort_key(chat): return chat.name
    chats = db.get_all_chats(Session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key),
    )


@chats_router.get("/{chat_id}", response_model=UsersAndMessagesAndChats, response_model_exclude_none=True)
def get_chat_by_id(chat_id: int, include: list[str] = Query([]),Session = Depends(db.get_session)):
    """"Get a chat by a certain id"""  
    chat =db.get_chat_by_id(Session, chat_id)
    users = chat.users
    messages = chat.messages
    if not include:
        users = None
        messages = None
    else:
        if 'users' not in include:
            users = None
        if 'messages' not in include:
            messages = None
    
    return UsersAndMessagesAndChats(
        meta=ChatMetaData(message_count=len(chat.messages), user_count=len(chat.users)),
        chat=chat,
        messages=messages,
        users=users
    )

@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: int, chat_update: ChatUpdate, Session = Depends(db.get_session)):
    """Updates a given chats name"""
    updated_chat = db.update_chat(Session, chat_id, chat_update)
    return ChatResponse(chat=updated_chat)


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_messages_by_id(chat_id: int, Session = Depends(db.get_session)):
    """Return a list of messages for a given id"""
    messages = db.get_messages_by_id(Session, chat_id)
    def sort_key(message): return getattr(message, "created_at")
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key)
    )


@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_chats_users(chat_id: int, Session = Depends(db.get_session)):
    """Return a list of users per chat"""

    user_list = []
    chat = db.get_chat_by_id(Session, chat_id)
    def sort_key(user): return getattr(user, "id")
    for user_id in chat.users:
        user_list.append(user_id)
    return UserCollection(
        meta={"count": len(user_list)},
        users=sorted(user_list, key=sort_key)
    )


@chats_router.post("/{chat_id}/messages", response_model=MessageResponse, status_code=201)
def create_new_message(new_message:CreateMessage, chat_id: int, current_user: UserInDB = Depends(auth_get_current_user), Session = Depends(db.get_session)):
    """Creates a new message for the current user and the given chat"""
    chat = db.get_chat_by_id(Session, chat_id)
    message = MessageInDB(text = new_message.text, user_id=current_user.id,chat_id=chat_id)
    Session.add(message)
    chat.messages.append(message)
    Session.commit()
    
    return MessageResponse(message=message)
    
