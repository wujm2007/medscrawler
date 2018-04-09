from sqlalchemy import String, Column

from medscrawler.models.entity import Entity


class Examination(Entity):
    name = Column(String(50))
