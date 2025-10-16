from datetime import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from ..models.token_expired import ExpiredToken


def add_token_to_blocklist(db: Session, jti: str, expires_at: datetime):
    stmt = insert(ExpiredToken).values(jti=jti, expires_at=expires_at)
    stmt = stmt.on_conflict_do_nothing(index_elements=["jti"])
    db.execute(stmt)
    db.commit()


def is_token_blocklisted(db: Session, jti: str) -> bool:
    return db.query(ExpiredToken).filter(ExpiredToken.jti == jti).first() is not None
