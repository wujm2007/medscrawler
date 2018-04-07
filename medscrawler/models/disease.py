from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from medscrawler.models.entity import Entity


class Disease(Entity):
    name_cn = Column(String)
    alias = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    position = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    departments = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    infectious = Column(Boolean)
    cure = Column(String)
    cure_rate = Column(String)
    cure_period = Column(String)
    susceptible_population = Column(String)
    fee = Column(String)
    typical_symptoms = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    clinical_examination = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    complication = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
    surgery = Column(MutableList.as_mutable(JSONB), default=[], server_default='[]')
