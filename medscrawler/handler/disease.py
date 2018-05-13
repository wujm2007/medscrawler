import json

from medscrawler.models import transaction
from medscrawler.models.department import Department
from medscrawler.models.disease import Disease
from medscrawler.models.disease_alias import DiseaseAlias
from medscrawler.models.disease_complication import DiseaseComplication
from medscrawler.models.disease_department import DiseaseDepartment
from medscrawler.models.disease_examination import DiseaseExamination
from medscrawler.models.disease_postition import DiseasePosition
from medscrawler.models.disease_surgery import DiseaseSurgery
from medscrawler.models.disease_symptiom import DiseaseSymptom
from medscrawler.models.examination import Examination
from medscrawler.models.postion import Position
from medscrawler.models.surgery import Surgery
from medscrawler.models.symptom import Symptom


def make_list(obj):
    return obj if isinstance(obj, list) else ([obj] if obj else [])


def bulk_import(diseases: list) -> None:
    all_diseases = {}
    all_positions = {}
    all_departments = {}
    all_symptoms = {}
    all_examinations = {}
    all_surgeries = {}
    for diseases in diseases:
        for name, info in diseases.items():
            try:
                with transaction():
                    disease = Disease.add(
                        name_cn=name,
                        infectious=bool(info.get('传染性') != '无传染性'),
                        cure=info.get('治疗方法'),
                        cure_rate=info.get('治愈率'),
                        cure_period=info.get('治疗周期'),
                        susceptible_population=info.get('多发人群'),
                        fee=info.get('治疗费用'),
                        surgery=make_list(info.get('手术')),
                    )
                    all_diseases[name] = disease.id

                    aliases = make_list((info.get('别名') or '').split(','))
                    for i in aliases:
                        if i:
                            DiseaseAlias.add(disease_id=disease.id, alias=i)
                            all_diseases[i] = disease.id

                    positions = make_list(info.get('发病部位', []))
                    for i in positions:
                        if i:
                            if i not in all_positions:
                                all_positions[i] = Position.add(name=i).id
                            if disease.id != all_positions[i]:
                                DiseasePosition.add(disease_id=disease.id, position_id=all_positions[i])

                    departments = make_list(info.get('挂号的科室', []))
                    for i in departments:
                        if i:
                            if i not in all_departments:
                                all_departments[i] = Department.add(name=i).id
                            DiseaseDepartment.add(disease_id=disease.id, department_id=all_departments[i])

                    symptoms = make_list(info.get('典型症状', []))
                    for i in symptoms:
                        if i:
                            if i not in all_symptoms:
                                all_symptoms[i] = Symptom.add(name=i).id
                            DiseaseSymptom.add(disease_id=disease.id, symptom_id=all_symptoms[i])

                    examinations = make_list(info.get('临床检查', []))
                    for i in examinations:
                        if i:
                            if i not in all_examinations:
                                all_examinations[i] = Examination.add(name=i).id
                            DiseaseExamination.add(disease_id=disease.id, examination_id=all_examinations[i])

                    surgeries = make_list(info.get('手术', []))
                    for i in surgeries:
                        if i:
                            if i not in all_surgeries:
                                all_surgeries[i] = Surgery.add(name=i).id
                            DiseaseSurgery.add(disease_id=disease.id, surgery_id=all_surgeries[i])

                    complication = make_list(info.get('并发症', []))
                    for i in complication:
                        if i:
                            if i in all_diseases:
                                DiseaseComplication.add(disease_id=disease.id, complication_id=all_diseases[i])
            except:
                pass


def import_from_file(path: str) -> None:
    diseases = []
    with open(path, encoding='utf-8') as file:
        for line in file:
            diseases.append(json.loads(line))
    bulk_import(diseases)


def dump_dict(path: str) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        for disease in Disease.all():
            file.write("{} n\n".format(disease.name_cn))
