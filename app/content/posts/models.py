from sqlalchemy import text, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column
from app.content.database import Base, str_uniq, int_pk
from datetime import date

class Post(Base):
    id: Mapped[int_pk]
    author_id: Mapped[int]

    title: Mapped[str]
    description: Mapped[str]
    # create_date: Mapped[date]
    # update_date: Mapped[date]

    is_private: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    tags : Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    def __str__(self):
        return (f"{self.__class__.__name__}(title={self.title}, "
                f"description={self.description!r},"
                f"author_id={self.author_id!r})")

    def __repr__(self):
        return str(self)