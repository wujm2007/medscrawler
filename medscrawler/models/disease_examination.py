from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity
from medscrawler.models.examination import Examination


class DiseaseExamination(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    examination_id = Column(Integer, ForeignKey(Examination.id), nullable=False)
