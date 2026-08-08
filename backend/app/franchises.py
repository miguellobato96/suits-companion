from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.franchise_repository import get_franchises
from app.franchise_models import FranchiseModel
from app.franchise_schemas import Franchise


router = APIRouter(
    prefix="/franchises",
    tags=["franchises"],
)


@router.get(
    "/",
    response_model=list[Franchise],
)
def list_franchises(
    db: Session = Depends(get_db),
) -> list[FranchiseModel]:
    return get_franchises(db)