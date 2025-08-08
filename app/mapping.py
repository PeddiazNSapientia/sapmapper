from app.database import SessionLocal
from app.models import Mapping, MappingCreate

def save_mapping(mapping_data: MappingCreate):
    db = SessionLocal()
    mapping = Mapping(**mapping_data.dict())
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    db.close()
    return mapping

def get_mappings(entity: str):
    db = SessionLocal()
    mappings = db.query(Mapping).filter(Mapping.sap_entity == entity).all()
    db.close()
    return mappings