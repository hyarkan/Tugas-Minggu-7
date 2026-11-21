from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scheduling import JadwalInput, JadwalResponse
from app.services.scheduling_service import SchedulingError, SchedulingService

router = APIRouter(prefix="/api/jadwal", tags=["Jadwal dan Ruangan"])

def _run(call):
    try:
        return call()
    except SchedulingError as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.body()})

@router.post("", status_code=201, response_model=JadwalResponse)
def create_jadwal(data: JadwalInput, db: Session = Depends(get_db)):
    return _run(lambda: SchedulingService(db).create(data))

@router.put("/{jadwal_id}", response_model=JadwalResponse)
def update_jadwal(jadwal_id: int, data: JadwalInput, db: Session = Depends(get_db)):
    return _run(lambda: SchedulingService(db).update(jadwal_id, data))

@router.delete("/{jadwal_id}", status_code=204)
def delete_jadwal(jadwal_id: int, db: Session = Depends(get_db)):
    result = _run(lambda: SchedulingService(db).delete(jadwal_id))
    return result

@router.get("/conflicts")
def list_conflicts(db: Session = Depends(get_db)):
    return [{"type": c.type, "affected": list(c.affected)} for c in SchedulingService(db).conflicts()]
