from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity
from medscrawler.models.medicine import Medicine


class Cure(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('disease_id', 'medicine_id'),
    )
