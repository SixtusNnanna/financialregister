import os
from datetime import date
from decimal import Decimal
from uuid import UUID
from typing import Annotated
from dotenv import load_dotenv

from starlette.middleware.sessions import SessionMiddleware
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.database.session import get_db, create_table
from app.database.models import Game, PaymentMode, Role, Transaction, Status, User
from app.service.transaction import TransactionService
from app.service.user import UserService
from app.api.deps import require_roles

load_dotenv()

app = FastAPI(title="Valhala Games")
templates = Jinja2Templates(directory="templates")

secrets = os.getenv("SECRETS")

app.add_middleware(
    SessionMiddleware,
    secret_key=secrets,
    max_age=3600,
    https_only=False,
    same_site="lax",
)


@app.on_event("startup")
def startup():
    create_table()


@app.get("/", response_class=HTMLResponse)
def new_transaction(
    request: Request,
    _current_user: Annotated[
        User, Depends(require_roles(Role.STAFF, Role.ADMIN))
    ],
    session: Session = Depends(get_db),
):
    games = (
        session.query(Game)
        .filter(Game.status == "available")
        .order_by(Game.name)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "games": games,
            "payment_modes": list(PaymentMode),
            "user": _current_user
        },
    )


@app.post("/")
def create_transaction(
    request: Request,
    _current_user: Annotated[
            User, Depends(require_roles(Role.STAFF, Role.ADMIN))
        ],
    game_id: UUID = Form(...),
    amount: Decimal = Form(..., gt=0),
    payment_mode: PaymentMode = Form(...),
    session: Session = Depends(get_db),
):
    game = session.query(Game).filter(
        Game.id == game_id
    ).first()

    if game is None or game.status == "unavailable":
        raise HTTPException(
            status_code=404,
            detail="Game not found or unavailable",
        )

    transaction = Transaction(
        game_id=game_id,
        amount=amount,
        payment_mode=payment_mode,
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    if transaction:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "message": "Transaction added successfully"
            }
        )


@app.post("/game/new", response_class=HTMLResponse)
def new_game(
    _current_user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],
    name: str = Form(...),
    description: str = Form(...),
    status: Status = Form(...),
    db: Session = Depends(get_db)
):
    new_game = Game(
        name=name,
        description=description,
        status=status
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return RedirectResponse(
        url="/",
        status_code=303,
        )


@app.get("/game/new", response_class=HTMLResponse)
def add_game(
    request: Request,
    _current_user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request=request,
        name="add_game.html",
        context={
            "status": list(Status),
            "user": _current_user
        }
    )


@app.get("/transactions", response_class=HTMLResponse)
def history(
    request: Request,
    _current_user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],
    db: Annotated[Session, Depends(get_db)]
):
    games = db.query(Game).order_by(Game.name).all()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "transactions": [],
            "total": 0,
            "games": games,
            "payment_modes": list(PaymentMode),
            "selected_game_id": "",
            "selected_date": "",
            "selected_payment_mode": "",
            "user": _current_user
        }
    )


@app.post("/transactions", response_class=HTMLResponse)
def transaction_history(
    request: Request,
    _current_user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],
    db: Annotated[Session, Depends(get_db)],
    game_id: Annotated[UUID | None, Form()] = None,
    transaction_date: Annotated[date | None, Form()] = None,
    payment_mode: Annotated[PaymentMode | None, Form()] = None,
):
    service = TransactionService(db)

    result = service.get_transactions_with_total(
        game_id=game_id,
        transaction_date=transaction_date,
        payment_mode=payment_mode,
    )

    games = db.query(Game).order_by(Game.name).all()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "transactions": result["transactions"],
            "total": result["total"],
            "games": games,
            "payment_modes": list(PaymentMode),
            "selected_game_id": str(game_id) if game_id else "",
            "selected_date": (
                transaction_date.isoformat()
                if transaction_date else ""
            ),
            "selected_payment_mode": (
                payment_mode.value if payment_mode else ""
            ),
            "user": _current_user
        },
    )


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request, user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],):
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context=get_template_context(
            request,
            user
        )
    )


@app.post("/signup")
def create_account(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    _current_user: Annotated[
            User, Depends(require_roles(Role.ADMIN))
        ],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)

    try:
        service.signup(
            username=username,
            password=password,
            role=Role.STAFF,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return RedirectResponse(
        url="/",
        status_code=303,
    )


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@app.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],
    db: Annotated[Session, Depends(get_db)],
):
    service = UserService(db)

    user = service.authenticate(
        username=form_data.username,
        password=form_data.password,
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid username or password."
            },
            status_code=401,
        )

    request.session["user_id"] = str(user.id)
    return RedirectResponse(
        url="/",
        status_code=303,
    )


@app.get("/logout")
def logout(request: Request, _current_user: Annotated[
        User, Depends(require_roles(Role.ADMIN, Role.STAFF))
    ],):
    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303,
    )


def get_template_context(
    request: Request,
    user,
    **extra,
):
    return {
        "request": request,
        "user": user,
        **extra,
    }
