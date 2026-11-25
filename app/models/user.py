from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    # Unique user ID
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Username
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # Email address
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # Hashed password only
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # User role
    role: Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False
    )

    # Account status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # Account creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )