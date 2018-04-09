from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity


class DiseaseComplication(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    complication_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
