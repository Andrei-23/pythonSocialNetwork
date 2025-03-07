from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date

class User(Base):
    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    password: Mapped[str]

    phone_number: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    email: Mapped[str_uniq]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)