from sqlalchemy.orm import Session
from app.database.models import Role, User
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


class UserService:

    def __init__(self, session: Session):
        self.session = session

    def signup(
            self,
            username: str,
            password: str,
            role: Role
    ):
        existing_user = self.get_user(
            username=username
        )
        if existing_user:
            raise ValueError("User already Exist")
        hashed_pw = pwd_context.hash(password)
        new_user = User(
            username=username,
            hashed_password=hashed_pw,
            role=role
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def get_user(self, username: str):
        return (
            self.session.query(User)
            .filter(User.username == username)
            .first()
        )

    def authenticate(self, username: str, password: str):
        user = self.get_user(username=username)
        if not user:
            return
        if not pwd_context.verify(password, user.hashed_password):
            return
        return user






