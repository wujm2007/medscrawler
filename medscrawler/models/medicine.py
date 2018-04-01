from sqlalchemy import Column, String

from medscrawler.models.entity import Entity


class Medicine(Entity):
    name_cn = Column(String)
    name_en = Column(String)
    ingredients = Column(String)
    indications = Column(String)
    usage = Column(String)
    unusual_reactions = Column(String)
    contraindication = Column(String)
    special_use = Column(String)
    storage = Column(String)
    note = Column(String)
    drug_interaction = Column(String)
    pharmacological_action = Column(String)
    expire_date = Column(String)
    license_number = Column(String)
    manufacturer = Column(String)
