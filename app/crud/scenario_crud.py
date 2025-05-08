from sqlalchemy.orm import Session
from app.model.scenario_model import Scenario

def get_all_scenarios(db: Session):
    return db.query(Scenario).all()