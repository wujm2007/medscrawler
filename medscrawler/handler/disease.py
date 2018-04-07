import json

from medscrawler.models import transactional
from medscrawler.models.disease import Disease


def make_list(obj):
    return obj if isinstance(obj, list) else ([obj] if obj else [])


@transactional
def bulk_import(diseases: list, session) -> None:
    for diseases in diseases:
        for name, info in diseases.items():
            instance = Disease(
                name_cn=name,
                alias=make_list((info.get('别名') or '').split(',')),
                position=make_list(info.get('发病部位')),
                departments=make_list(info.get('挂号的科室')),
                infectious=bool(info.get('传染性') != '无传染性'),
                cure=info.get('治疗方法'),
                cure_rate=info.get('治愈率'),
                cure_period=info.get('治疗周期'),
                susceptible_population=info.get('多发人群'),
                fee=info.get('治疗费用'),
                typical_symptoms=make_list(info.get('典型症状')),
                clinical_examination=make_list(info.get('临床检查')),
                complication=make_list(info.get('并发症')),
                surgery=make_list(info.get('手术')),
            )
            session.add(instance)


def import_from_file(path: str) -> None:
    diseases = []
    with open(path, encoding='utf-8') as file:
        for line in file:
            diseases.append(json.loads(line))
    bulk_import(diseases)
