from sqlalchemy.orm import Session

from rag_system_basic.rag_system.app.database.models import (
    User,
    Conversation,
    Message,
    UploadedDocument
)


# =========================
# USER
# =========================

def create_user(
    db: Session,
    username,
    email,
    hashed_password
):

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def get_user_by_email(
    db: Session,
    email
):

    return db.query(User).filter(
        User.email == email
    ).first()


# =========================
# CONVERSATION
# =========================

def create_conversation(
    db: Session,
    user_id,
    title
):

    conversation = Conversation(
        user_id=user_id,
        title=title
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation


# =========================
# MESSAGE
# =========================

def save_message(
    db: Session,
    conversation_id,
    role,
    content
):

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id
):

    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()


# =========================
# DOCUMENT
# =========================

def save_uploaded_document(
    db: Session,
    filename,
    file_path,
    user_id
):

    document = UploadedDocument(
        filename=filename,
        file_path=file_path,
        user_id=user_id
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return document