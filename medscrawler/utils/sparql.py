from SPARQLWrapper import SPARQLWrapper, JSON


def request(query: str, endpoint="http://localhost:3030/kg/sparql") -> tuple:
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["head"]["vars"], [(v['value'] for k, v in d.items()) for d in results["results"]["bindings"]]


KEY_MAPPING = {
    'answer': '答案',
    'medicine_name_cn': '药品名称',
    'medicine_indications': '作用',
    'medicine_ingredients': '药品成分',
    'medicine_manufacturer': '生产厂商',
    'medicine_contraindication': '禁忌',
    'medicine_drug_interaction': '药物相互作用',
    'medicine_unusual_reactions': '不良反应',
    'medicine_expire_date': '有效期',
    'medicine_special_use': '特殊使用',
    'medicine_storage': '贮藏',
    'medicine_usage': '使用方法',
    'medicine_note': '说明',
    'medicine_pharmacological_action': '药理作用',
    'disease_cure_rate': '治愈率',
    'disease_cure': '治疗方法',
    'disease_name_cn': '疾病名称',
    'disease_susceptible_population': '易感人群',
    'disease_fee': '治疗费用',
    'disease_infectious': '传染性',
    'symptom': '症状',
    'position': '发病部位',
}


def key_mapping(d: dict) -> dict:
    def _map(k: str) -> str:
        k_ = k.split('#')[-1]
        return KEY_MAPPING.get(k_)

    print(d)
    return {_map(k): v for k, v in d.items() if _map(k)}


def res_format(vars_: list, bindings_: list) -> dict:
    bindings_ = [list(v) for v in bindings_]
    if not vars_:
        return key_mapping({'answer': "我不知道"})
    elif len(vars_) == 1:
        return key_mapping({vars_[0]: ','.join([v[0] for v in bindings_])})
    else:
        bindings_ = bindings_[:]
        return key_mapping({v[1]: v[2] for v in bindings_})
