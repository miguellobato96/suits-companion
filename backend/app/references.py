from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.franchise_models import FranchiseModel
from app.media_models import MediaModel
from app.reference_models import ReferenceModel
from app.reference_repository import (
    character_exists,
    count_references,
    create_reference,
    delete_reference,
    get_franchises_by_ids,
    get_media_by_ids,
    get_reference,
    get_references,
    patch_reference,
    update_reference,
)
from app.reference_schemas import (
    Reference,
    ReferenceCreate,
    ReferenceListResponse,
    ReferencePatch,
    ReferenceType,
    ReferenceUpdate,
)


router = APIRouter(
    prefix="/references",
    tags=["references"],
)


def resolve_media(
    db: Session,
    media_ids: list[int],
) -> list[MediaModel]:
    media = get_media_by_ids(db, media_ids)

    requested_ids = set(media_ids)
    found_ids = {item.id for item in media}

    missing_ids = sorted(requested_ids - found_ids)

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Media does not exist: {missing_ids}",
        )

    return media


def resolve_franchises(
    db: Session,
    franchise_ids: list[int],
) -> list[FranchiseModel]:
    franchises = get_franchises_by_ids(db, franchise_ids)

    requested_ids = set(franchise_ids)
    found_ids = {item.id for item in franchises}

    missing_ids = sorted(requested_ids - found_ids)

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Franchise does not exist: {missing_ids}",
        )

    return franchises


@router.get(
    "/",
    response_model=ReferenceListResponse,
)
def list_references(
    search: str | None = Query(default=None),
    reference_type: ReferenceType | None = Query(default=None),
    character_id: int | None = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> ReferenceListResponse:
    items = get_references(
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
        items=items,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{reference_id}",
    response_model=Reference,
)
def read_reference(
    reference_id: int,
    db: Session = Depends(get_db),
) -> ReferenceModel:
    reference = get_reference(db, reference_id)

    if reference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    return reference


@router.post(
    "/",
    response_model=Reference,
    status_code=status.HTTP_201_CREATED,
)
def create_reference_endpoint(
    data: ReferenceCreate,
    db: Session = Depends(get_db),
) -> ReferenceModel:
    if not character_exists(db, data.spoken_by_character_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character does not exist",
        )

    media = resolve_media(db, data.media_ids)
    franchises = resolve_franchises(db, data.franchise_ids)

    return create_reference(
        db=db,
        data=data,
        media=media,
        franchises=franchises,
    )


@router.put(
    "/{reference_id}",
    response_model=Reference,
)
def update_reference_endpoint(
    reference_id: int,
    data: ReferenceUpdate,
    db: Session = Depends(get_db),
) -> ReferenceModel:
    reference = get_reference(db, reference_id)

    if reference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    if not character_exists(db, data.spoken_by_character_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character does not exist",
        )

    media = resolve_media(db, data.media_ids)
    franchises = resolve_franchises(db, data.franchise_ids)

    return update_reference(
        db=db,
        reference=reference,
        data=data,
        media=media,
        franchises=franchises,
    )


@router.patch(
    "/{reference_id}",
    response_model=Reference,
)
def patch_reference_endpoint(
    reference_id: int,
    data: ReferencePatch,
    db: Session = Depends(get_db),
) -> ReferenceModel:
    reference = get_reference(db, reference_id)

    if reference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    updates = data.model_dump(exclude_unset=True)

    character_id = updates.get("spoken_by_character_id")

    if (
        character_id is not None
        and not character_exists(db, character_id)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Character does not exist",
        )

    update_media = "media_ids" in updates
    media = None

    if update_media:
        media_ids = updates.pop("media_ids") or []
        media = resolve_media(db, media_ids)

    update_franchises = "franchise_ids" in updates
    franchises = None

    if update_franchises:
        franchise_ids = updates.pop("franchise_ids") or []
        franchises = resolve_franchises(db, franchise_ids)

    return patch_reference(
        db=db,
        reference=reference,
        updates=updates,
        media=media,
        franchises=franchises,
        update_media=update_media,
        update_franchises=update_franchises,
    )


@router.delete(
    "/{reference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reference_endpoint(
    reference_id: int,
    db: Session = Depends(get_db),
) -> Response:
    reference = get_reference(db, reference_id)

    if reference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reference not found",
        )

    delete_reference(db, reference)

    return Response(status_code=status.HTTP_204_NO_CONTENT)