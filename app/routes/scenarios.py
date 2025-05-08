from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.scenario_crud import get_all_scenarios
from app.schema.scenario_schema import ScenarioOut
from typing import List

router = APIRouter()

@router.get("/scenarios", response_model=List[ScenarioOut])
def fetch_scenarios(db: Session = Depends(get_db)):
    return get_all_scenarios(db)