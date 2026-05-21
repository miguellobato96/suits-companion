from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.reference_repository import (
    character_exists,
    count_references,
    create_new_reference,
    delete_existing_reference,
    get_all_references,
    get_reference_by_id,
    patch_existing_reference,
    update_existing_reference,
)
from app.reference_schemas import (
    Reference,
    ReferenceCreate,
    ReferenceListResponse,
    ReferencePatch,
    ReferenceType,
    ReferenceUpdate,
)

router = APIRouter(prefix="/references", tags=["References"])


@router.get("/", response_model=ReferenceListResponse)
def get_references(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    reference_type: ReferenceType | None = Query(default=None),
    character_id: int | None = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> ReferenceListResponse:
    references = get_all_references(
        db=db,
        search=search,
        reference_type=reference_type,
        character_id=character_id,
        offset=offset,
        limit=limit,
    )
    total = count_references(
        db=db,
        search=search,
        reference_type=reference_type,
        character_id=character_id,
    )

    return ReferenceListResponse(
        items=references,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{reference_id}", response_model=Reference)
def get_reference(
    reference_id: int,
    db: Session = Depends(get_db),
) -> Reference:
    reference = get_reference_by_id(db, reference_id)

    if reference is None:
        raise HTTPException(status_code=404, detail="Reference not found")

    return reference


@router.post("/", response_model=Reference, status_code=status.HTTP_201_CREATED)
def create_reference(
    reference_data: ReferenceCreate,
    db: Session = Depends(get_db),
) -> Reference:
    if not character_exists(db, reference_data.spoken_by_character_id):
        raise HTTPException(status_code=400, detail="Character does not exist")

    return create_new_reference(db, reference_data)


@router.put("/{reference_id}", response_model=Reference)
def update_reference(
    reference_id: int,
    reference_data: ReferenceUpdate,
    db: Session = Depends(get_db),
) -> Reference:
    reference = get_reference_by_id(db, reference_id)

    if reference is None:
        raise HTTPException(status_code=404, detail="Reference not found")

    if not character_exists(db, reference_data.spoken_by_character_id):
        raise HTTPException(status_code=400, detail="Character does not exist")

    updated_reference = update_existing_reference(db, reference_id, reference_data)

    if updated_reference is None:
        raise HTTPException(status_code=404, detail="Reference not found")

    return updated_reference


@router.patch("/{reference_id}", response_model=Reference)
def patch_reference(
    reference_id: int,
    reference_data: ReferencePatch,
    db: Session = Depends(get_db),
) -> Reference:
    reference = get_reference_by_id(db, reference_id)

    if reference is None:
        raise HTTPException(status_code=404, detail="Reference not found")

    if (
        reference_data.spoken_by_character_id is not None
        and not character_exists(db, reference_data.spoken_by_character_id)
    ):
        raise HTTPException(status_code=400, detail="Character does not exist")

    updated_reference = patch_existing_reference(db, reference_id, reference_data)

    if updated_reference is None:
        raise HTTPException(status_code=404, detail="Reference not found")

    return updated_reference


@router.delete("/{reference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reference(
    reference_id: int,
    db: Session = Depends(get_db),
) -> None:
    deleted = delete_existing_reference(db, reference_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Reference not found")

    return None