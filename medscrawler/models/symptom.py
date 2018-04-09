from sqlalchemy import String, Column

from medscrawler.models.entity import Entity


class Symptom(Entity):
    name = Column(String(30))
