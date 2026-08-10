from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.franchises.model import FranchiseModel
from app.franchises.repository import get_franchises
from app.franchises.schemas import Franchise

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
