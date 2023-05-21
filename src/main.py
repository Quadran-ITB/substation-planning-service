from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .config import Settings
from .database import SessionLocal, engine
from .models import models
from .crud import crud_region, crud_gardu_induk
from .schemas import area, gardu_induk

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
settings = Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/available-gardu-induk", response_model=gardu_induk.ReadGarduInduk)
async def gardu_induk_list(db: Session = Depends(get_db)):
    result = crud_gardu_induk.get_gardu_induk(db)
    print(result)

    data = {
        "available": result,
    }

    return gardu_induk.ReadGarduInduk(**data)


@app.get("/area", response_model=area.ReadArea)
async def main_substation_area(method: str, area_name: str, db: Session = Depends(get_db)):
    area_result = crud_region.calculate_gi_region(db, gi_name=area_name, calc_method=method)

    data = {
        "GI": area_name,
        "area": area_result,
    }

    return area.ReadArea(**data)


# TODO
@app.get("/total")
async def load_point_total():
    return {"message": "Endpoint Total Titik Beban"}


# TODO
@app.get("/capacity")
async def load_point_capacity():
    return {"message": "Endpoint Rekap Titik Beban"}


# TODO
@app.get("/density")
async def main_substation_density():
    return {"message": "Endpoint Kerapatan GI"}