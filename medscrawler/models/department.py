from sqlalchemy import String, Column

from medscrawler.models.entity import Entity


class Department(Entity):
    name = Column(String(20))
