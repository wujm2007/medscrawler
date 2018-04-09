from sqlalchemy import Column, Integer, ForeignKey

from medscrawler.models.department import Department
from medscrawler.models.disease import Disease
from medscrawler.models.entity import Entity


class DiseaseDepartment(Entity):
    disease_id = Column(Integer, ForeignKey(Disease.id), nullable=False)
    department_id = Column(Integer, ForeignKey(Department.id), nullable=False)
