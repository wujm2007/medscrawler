from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity
from medscrawler.models.symptom import Symptom


class DiseaseSymptom(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    symptom_id = Column(Integer, ForeignKey(Symptom.id), nullable=False)
