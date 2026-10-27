from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.database.models import PaymentMode, Status

class GameBase(BaseModel):
    name: str
    description: str
    status: Status


class GamesCreate(GameBase):
    pass


class GameRead(GameBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class transactionBase(BaseModel):
    game_id: UUID
    amount: Decimal
    payment_mode: PaymentMode


class TransactionCreate(transactionBase):
    pass


class TransactionRead(transactionBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


