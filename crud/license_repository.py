from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.license_repository import LicenseRepository
from ..schemas.license_repository import LicenseRepositoryCreate, LicenseRepositoryUpdate
import uuid


def create_license_repository(
    db: Session, 
    license_repo: LicenseRepositoryCreate
) -> LicenseRepository:
    """라이센스 저장소 생성"""
    # ULID 생성 (고유한 ID)
    license_id = str(uuid.uuid4())
    
    # 데이터베이스 객체 생성
    db_license_repo = LicenseRepository(
        id=license_id,
        name=license_repo.name,
        description=license_repo.description,
        registrant_name=license_repo.registrant_name,
        github_url=license_repo.github_url,
        copyright_owner=license_repo.copyright_owner,
        license_info=license_repo.license_info
    )
    
    # 데이터베이스에 저장
    db.add(db_license_repo)     # 메모리에만 객체 추가 -> DB에는 저장되지 않음
    db.commit()                 # 실제로 DB에 영구 저장
    db.refresh(db_license_repo) # DB에서 최신 데이터를 다시 가져옴 -> 객체가 데이터베이스의 실제 상태와 동기화
                                # refresh 하지 않으면 created_at이 None으로 반환될 수 있음
    return db_license_repo


def get_license_repositories(db: Session) -> List[LicenseRepository]:
    """전체 라이센스 저장소 목록 조회"""
    return db.query(LicenseRepository).all()


def get_license_repository(db: Session, license_id: str) -> Optional[LicenseRepository]:
    """특정 라이센스 저장소 조회"""
    return db.query(LicenseRepository).filter(LicenseRepository.id == license_id).first()


def delete_license_repository(db: Session, license_id: str) -> bool:
    """라이센스 저장소 삭제"""
    license_repo = db.query(LicenseRepository).filter(LicenseRepository.id == license_id).first()
    
    if license_repo:
        db.delete(license_repo)
        db.commit()
        return True
    return False
