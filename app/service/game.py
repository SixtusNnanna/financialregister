from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Game, Status


class GameService:
    def __init__(self, session: Session):
        self.session = session

    def get_game_by_id(self, id: UUID):
        return self.session.get(Game, id)

    def get_all_games(self):
        stmt = select(Game)
        return self.session.execute(stmt).scalars().all()

    def add_game(self, name: str, description: str, status: Status):
        new_game = Game(
            name=name,
            description=description,
            status=status
        )
        self.session.add(new_game)
        self.session.commit()
        self.session.refresh(new_game)
        return new_game

    def change_game_status(self, id: UUID, status: Status):
        game = self.get_game_by_id(id)
        if game is None:
            return
        game.status = status
        self.session.commit()
        self.session.refresh(game)
        return game
