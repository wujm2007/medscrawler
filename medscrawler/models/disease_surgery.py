from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity
from medscrawler.models.surgery import Surgery


class DiseaseSurgery(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    surgery_id = Column(Integer, ForeignKey(Surgery.id), nullable=False)
