from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.scenario_crud import get_all_scenarios, get_scenario_by_id
from app.schema.scenario_schema import ScenarioOut
from typing import List

router = APIRouter()

@router.get("/scenarios", response_model=List[ScenarioOut])
def fetch_scenarios(db: Session = Depends(get_db)):
    return get_all_scenarios(db)

@router.get("/scenarios/{scenario_id}", response_model=ScenarioOut)
def fetch_scenario_by_id(scenario_id: int, db: Session = Depends(get_db)):
    scenario = get_scenario_by_id(db, scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario