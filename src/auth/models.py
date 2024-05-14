from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import mapped_column, Mapped
from database import Base, metadata

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String(length=320), unique=True, index=True, nullable=False),
#     Column('email', String(length=320), unique=True, index=True, nullable=False),
#     Column('hashed_password', String(length=1024), nullable=False),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column('is_superuser', Boolean, default=False, nullable=False),
#     Column('is_verified', Boolean, default=False, nullable=False),
#     Column('created_at', TIMESTAMP, default=datetime.utcnow),
#     Column('role_id', Integer, ForeignKey(role.c.id)),
#
# )


# Для fastapi_users згідно її вимог!
class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(role.c.id), nullable=False
    )
