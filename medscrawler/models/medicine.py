from sqlalchemy import Column, String, Text

from medscrawler.models.entity import Entity


class Medicine(Entity):
    name_cn = Column(String(100))
    name_en = Column(String(200))
    ingredients = Column(Text)
    indications = Column(Text)
    usage = Column(Text)
    unusual_reactions = Column(Text)
    contraindication = Column(Text)
    special_use = Column(Text)
    storage = Column(String(200))
    note = Column(Text)
    drug_interaction = Column(Text)
    pharmacological_action = Column(Text)
    expire_date = Column(String(100))
    license_number = Column(String(50))
    manufacturer = Column(String(200))
