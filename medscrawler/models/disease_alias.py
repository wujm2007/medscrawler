from sqlalchemy import Column, Integer, String, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity


class DiseaseAlias(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    alias = Column(String(100))
