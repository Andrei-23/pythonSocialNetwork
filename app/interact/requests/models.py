import datetime
from sqlalchemy import text, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column
from app.interact.database import Base, str_uniq, int_pk
from datetime import date

class UserRegisterInfo(Base):
    user_id: Mapped[int]

class InteractionData(Base):
    user_id: Mapped[int]
    post_id: Mapped[int]

class CommentData(Base):
    user_id: Mapped[int]
    post_id: Mapped[int]
    comment: Mapped[str]
