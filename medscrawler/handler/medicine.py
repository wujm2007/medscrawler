import json
import re

from medscrawler.models import transactional
from medscrawler.models.medicine import Medicine


def parse_name(name_str: str) -> tuple:
    matched_general = re.search(r'通用名称：(.*)', name_str.strip(), re.M | re.I)
    matched_english = re.search(r'英文名称：(.*)', name_str.strip(), re.M | re.I)
    return (matched_general.group(1) if matched_general else '',
            matched_english.group(1) if matched_english else '')


@transactional
def bulk_import(meds: list) -> None:
    for med in meds:
        for _, med_info in med.items():
            name_cn, name_en = parse_name(med_info.get('药品名称', ''))
            Medicine.add(
                name_cn=name_cn,
                name_en=name_en,
                ingredients=med_info.get('成份'),
                indications=med_info.get('适应症'),
                usage=med_info.get('用法用量'),
                unusual_reactions=med_info.get('不良反应'),
                contraindication=med_info.get('禁忌'),
                special_use=med_info.get('特殊人群用药'),
                storage=med_info.get('贮藏'),
                note=med_info.get('注意事项'),
                drug_interaction=med_info.get('药物相互作用'),
                pharmacological_action=med_info.get('药理作用'),
                expire_date=med_info.get('有效期'),
                license_number=med_info.get('批准文号'),
                manufacturer=med_info.get('生产企业'),
            )


def import_from_file(path: str) -> None:
    meds = []
    with open(path, encoding='utf-8') as file:
        for line in file:
            meds.append(json.loads(line))
    bulk_import(meds)


def dump_dict(path: str) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        for disease in Medicine.all():
            file.write("{} nz\n".format(disease.name_cn))
