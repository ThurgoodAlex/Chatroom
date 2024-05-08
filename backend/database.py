import json
import os
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine, select


from backend.schema import(
    UserInDB, ChatInDB, 
    MessageInDB,  ChatUpdate, UserUpdate, ChatCollection
)

if os.environ.get("DB_LOCATION") == "EFS":
    db_path = "/mnt/efs/pony_express.db"
    echo = False
else:
    db_path = "backend/pony_express.db"
    echo = True

engine = create_engine(
    f"sqlite:///{db_path}",
    pool_pre_ping=True,
    echo=echo,
    connect_args={"check_same_thread": False},
    
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


class DuplicateEntityException(EntityNotFoundException):
    pass



def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return session.exec(select(UserInDB)).all()




def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
Retrieve an user from the database.

:param user_id: id of the user to be retrieved
:return: the retrieved user
:raises EntityNotFoundException: if no such user id exists
"""
    user = session.get(UserInDB, user_id)
    if user:
        return user
    raise EntityNotFoundException("User", user_id)


def get_users_chats(session: Session, user_id) -> ChatCollection:
    """
    retrieves chats for a given user
    """
    chats = get_all_chats(session)

    user_chats = []
    for chat in chats:
        if user_id in chat:
            user_chats.append(chat)
    if len(user_chats) == 0:
        raise EntityNotFoundException("User", user_id)
    print(user_chats)
    return user_chats




def get_all_chats(session: Session) -> list[ChatInDB]:
    """
    Retrieve all chats from the database.

    :return: ordered list of chats
    """


    return session.exec(select(ChatInDB)).all()


def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
    """
 Retrieve a chat from the database.

 :param chat_id: id of the chat to be retrieved
 :return: the retrieved chat
 :raises EntityNotFoundException: if no such chat id exists
 """

    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat
    raise EntityNotFoundException(entity_name="Chat",entity_id=chat_id)


def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update a chat in the database.

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated chat
    :raises EntityNotFoundException: if no such chat id exists
    """

    chat = get_chat_by_id(session, chat_id)
    for attr, value in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat,attr,value)
    session.commit()
    session.refresh(chat)
    return chat



def update_user(session: Session, current_user: UserInDB, user_update: UserUpdate) -> UserInDB:
    """Updates the current users username and or email"""
    for attr,value in user_update.model_dump(exclude_unset=True).items():
        print(attr)
        if attr != "id" and value != "string":
            setattr(current_user, attr, value)
    session.commit()
    session.refresh(current_user)
    return current_user
    

def get_messages_by_id(session: Session, chat_id:  int) -> list[MessageInDB]:
    """
    Get messages by id
    :param chat_id: the chat id to get the messages from
    :raises EntityNotFoundException: if no such chat exits
    """

    chat = get_chat_by_id(session,chat_id)
    return chat.messages
   
            
