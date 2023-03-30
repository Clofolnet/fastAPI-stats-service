from datetime import date
from typing import Any, List, Optional

import schemas
from api.crud import statistic as statistic_crud
from api.deps import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.Statistic])
def read_statistics(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
        Retrieve statistics.
    """
    statistics = statistic_crud.get_multi(db, skip=skip, limit=limit)
    return statistics


@router.post("/", response_model=schemas.Statistic)
def create_statistic(
    *,
    db: Session = Depends(get_db),
    statistic_in: schemas.StatisticCreate,
) -> Any:
    """
        Create new statistic.
    """
    statistic = statistic_crud.create(db=db, obj_in=statistic_in)
    return statistic


@router.get("/read-stats", response_model=List[schemas.StatisticForSee])
def read_stats(
    *,
    db: Session = Depends(get_db),
    from_date: date,
    to_date: date,
    views_sort: Optional[bool] = False,
    clicks_sort: Optional[bool] = False,
    cost_sort: Optional[bool] = False,
) -> Any:
    """
        Retrieve statistics filtered by date range and optional views, clicks, and cost.
    """
    results = statistic_crud.read_stats(db=db, from_date=from_date, to_date=to_date,
                                        views_sort=views_sort, clicks_sort=clicks_sort, cost_sort=cost_sort)
    return results


@router.get("/{id}", response_model=schemas.Statistic)
def read_statistic(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
        Get statistic by ID.
    """
    statistic = statistic_crud.get(db=db, id=id)
    if not statistic:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return statistic


@router.delete("/delete-all")
def delete_all_statistic(
    *,
    db: Session = Depends(get_db)
) -> Any:
    """
        Delete all statistics.
    """
    statistic_crud.delete_all(db=db)
    return {
        'success': True,
        'message': 'All entries deleted'
    }


@router.delete("/{id}", response_model=schemas.Statistic)
def delete_statistic(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
        Delete an statistic.
    """
    statistic = statistic_crud.get(db=db, id=id)
    if not statistic:
        raise HTTPException(status_code=404, detail="Statistic not found")
    statistic = statistic_crud.remove(db=db, id=id)
    return statistic
