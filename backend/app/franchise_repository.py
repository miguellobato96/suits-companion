from sqlalchemy import select
from sqlalchemy.orm import Session

from app.franchise_models import FranchiseModel


def get_franchises(db: Session) -> list[FranchiseModel]:
    statement = select(FranchiseModel).order_by(FranchiseModel.name)

    return list(db.scalars(statement).all())
