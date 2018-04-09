from sqlalchemy import String, Column

from medscrawler.models.entity import Entity


class Position(Entity):
    name = Column(String(20))
