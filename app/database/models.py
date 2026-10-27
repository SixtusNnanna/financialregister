from uuid import uuid4
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    Numeric,
    ForeignKey,
    Enum as SQLENUM,
    Uuid,
    DateTime,
)
from sqlalchemy.orm import relationship
from app.database.session import Base
from enum import Enum


class PaymentMode(Enum):
    BANK_TRANSFER = "bank_transfer"
    LANDMARK_APP = "landmark_app"
    UP_SIDE_DOWN_HOUSE = "upside_down_house"


class Status(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class Role(Enum):
    STAFF = "staff"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(200))
    role = Column(
            SQLENUM(
                Role,
                values_callable=lambda enum_cls: [
                    member.value for member in enum_cls
                ],
            ),
            default=Role.STAFF,
        )


class Game(Base):
    __tablename__ = "games"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(
        SQLENUM(
            Status,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=Status.AVAILABLE
    )
    transactions = relationship(
        "Transaction",
        back_populates="game",
        cascade="all, delete-orphan",
    )


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_mode = Column(
        SQLENUM(
            PaymentMode,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        nullable=False,
        default=PaymentMode.BANK_TRANSFER,
    )
    game_id = Column(
        Uuid(as_uuid=True), ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    created_at = Column(DateTime, default=(datetime.now()))
    game = relationship("Game", back_populates="transactions")
