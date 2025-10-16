from fastapi.exceptions import ValidationException
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import OAuthProvider
from ..utils.token import hash_password


def create_user(
    db: Session,
    email: str,
    name: str,
    password: str | None = None,
    oauth_provider: str | None = None,
):
    if oauth_provider and oauth_provider not in [item.value for item in OAuthProvider]:
        raise ValidationException(f"Invalid OAuth provider: {oauth_provider}")

    user = User(
        email=email,
        name=name,
        oauth_provider=oauth_provider,
    )
    if password:
        user.password_hash = hash_password(password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user():
    pass
