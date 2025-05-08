from pydantic import BaseModel

class ScenarioOut(BaseModel):
    id: int
    title: str
    imageurl: str
    role: str
    place: str

    class Config:
        orm_mode = True