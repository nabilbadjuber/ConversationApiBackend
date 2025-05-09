from sqlalchemy.orm import Session
from app.model.scenario_model import Scenario

def get_all_scenarios(db: Session):
    return db.query(Scenario).all()

def get_scenario_by_id(db: Session, scenario_id: int):
    return db.query(Scenario).filter(Scenario.id == scenario_id).first()