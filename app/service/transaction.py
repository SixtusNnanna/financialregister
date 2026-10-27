from uuid import UUID
from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.models import Transaction, PaymentMode
from datetime import datetime, time, timedelta, date


class TransactionService:
    def __init__(self, session: Session):
        self.session = session

    def get_transaction(self, transaction_id: UUID):
        return self.session.get(Transaction, id)

    def add_transaction(
            self,
            game_id: UUID,
            amount: Decimal,
            payment_mode: PaymentMode,
    ):
        new_tranaction = Transaction(
            game_id=game_id,
            amount=amount,
            payment_mode=payment_mode
        )
        self.session.add(new_tranaction)
        self.session.commit()
        self.session.refresh(new_tranaction)

    def edit_transaction_amount(self, transaction_id: UUID, amount: Decimal):
        transaction = self.get_transaction(transaction_id)
        if transaction is None:
            return
        transaction.amount = amount
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def edit_payment_mode(
        self,
        transaction_id: UUID,
        payment_mode: PaymentMode,
    ):
        transaction = self.get_transaction(transaction_id)
        if transaction is None:
            return
        transaction.payment_mode = payment_mode
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get_transactions_with_total(
        self,
        game_id: UUID | None = None,
        transaction_date: date | None = None,
        payment_mode: PaymentMode | None = None,
    ):
        query = self.session.query(Transaction)

        if game_id is not None:
            query = query.filter(Transaction.game_id == game_id)

        if transaction_date is not None:
            start = datetime.combine(transaction_date, time.min)
            end = start + timedelta(days=1)
            query = query.filter(
                Transaction.created_at >= start,
                Transaction.created_at < end,
            )
        if payment_mode is not None:
            query = query.filter(
                Transaction.payment_mode == payment_mode
            )

        total = query.with_entities(
            func.sum(Transaction.amount)
        ).scalar()

        transactions = query.order_by(
            Transaction.created_at.desc()
        ).all()
        return {
            "transactions": transactions,
            "total": total if total is not None else Decimal("0.00"),
        }
