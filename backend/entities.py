from datetime import date, datetime

from pydantic import BaseModel


class UserInDB(BaseModel):
    """Represents a user in the database."""

    id: int
    created_at: datetime


class User(BaseModel):
    "Represents an API response for a user"

    id: int
    created_at: datetime


class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


class UserCollection(BaseModel):
    "Represents an API response for a collection of users"
    meta: Metadata
    users: list[UserInDB]


class UserUpdate(BaseModel):
    """Represents parameters for updating a user in the system."""

    id: int = None
    created_at: datetime = None


class UserResponse(BaseModel):
    """"Represents a proper API response for a user"""
    user: UserInDB


class ChatInDB(BaseModel):
    """Represents a Chat in DB"""
    id: int
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime


class ChatResponse(BaseModel):
    """Represents a proper API response for a chat"""
    chat: ChatInDB


class Chat(BaseModel):
    """Represents an API call to a Chat"""
    id: int
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime


class ChatCollection(BaseModel):
    "Represents an API response for a collection of chats"
    meta: Metadata
    chats: list[ChatInDB]


class ChatUpdate(BaseModel):
    """Represents parameters for updating a chat in the system."""
    name: str = None


class Message(BaseModel):
    id: int
    user_id: str
    text: str
    created_at: datetime


class MessageInDB(BaseModel):
    id: int
    user_id: str
    text: str
    created_at: datetime


class MessageCollection(BaseModel):
    meta: Metadata
    messages: list[MessageInDB]
