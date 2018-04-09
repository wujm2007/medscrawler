from sqlalchemy import String, Column

from medscrawler.models.entity import Entity


class Surgery(Entity):
    name = Column(String(20))
