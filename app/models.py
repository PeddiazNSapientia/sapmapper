from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from app.database import Base

class Mapping(Base):
    __tablename__ = "mappings"
    id = Column(Integer, primary_key=True, index=True)
    sap_entity = Column(String, index=True)
    sap_field = Column(String)
    salesforce_field = Column(String)

class MappingCreate(BaseModel):
    sap_entity: str
    sap_field: str
    salesforce_field: str