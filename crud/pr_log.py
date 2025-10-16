from sqlalchemy.orm import Session
from app.models.pr_log import PRLog
from app.schemas.pr_log import PRLogCreate

def create_pr_log(db: Session, log_data: PRLogCreate):
    db_log = PRLog(**log_data.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
