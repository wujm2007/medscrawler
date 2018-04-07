import json

from medscrawler.models import transactional
from medscrawler.models.cure import Cure
from medscrawler.models.disease import Disease
from medscrawler.models.medicine import Medicine


@transactional
def bulk_import(objs: list, session) -> None:
    for obj in objs:
        for name, info in obj.items():
            for med in info.get('meds', []):
                disease = Disease.query_by_kwargs(name_cn=name).first()
                medicine = Medicine.query_by_kwargs(name_cn=med).first()
                if disease and medicine:
                    instance = Cure(
                        disease_id=disease.id,
                        medicine_id=medicine.id
                    )
                    session.add(instance)


def import_from_file(path: str) -> None:
    diseases = []
    with open(path, encoding='utf-8') as file:
        for line in file:
            diseases.append(json.loads(line))
    bulk_import(diseases)
