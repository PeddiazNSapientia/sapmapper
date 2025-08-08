from fastapi import FastAPI
from app.sap_service import get_entities, get_entity_fields
from app.mapping import save_mapping, get_mappings
from app.models import MappingCreate
from app.database import Base, engine
from xml.etree import ElementTree as ET


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/entities")
def entities_endpoint():
    return {"entities": get_entities()}


@app.get("/entities/{name}")
def entity_fields(name: str):
    return {"fields": get_entity_fields(name)}

@app.post("/map/salesforce")
def create_mapping(mapping: MappingCreate):
    return save_mapping(mapping)

@app.get("/map/salesforce/{entity}")
def read_mappings(entity: str):
    return get_mappings(entity)
