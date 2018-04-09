from sqlalchemy import Column, String, Boolean

from medscrawler.models.entity import Entity


class Disease(Entity):
    name_cn = Column(String(50))
    infectious = Column(Boolean)
    cure = Column(String(100))
    cure_rate = Column(String(50))
    cure_period = Column(String(30))
    susceptible_population = Column(String(150))
    fee = Column(String(50))
