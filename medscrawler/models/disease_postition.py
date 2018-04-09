from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity
from medscrawler.models.postion import Position


class DiseasePosition(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    position_id = Column(Integer, ForeignKey(Position.id), nullable=False)
