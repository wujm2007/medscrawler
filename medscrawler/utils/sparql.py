from SPARQLWrapper import SPARQLWrapper, JSON

from medscrawler.const import KEY_MAPPING
from medscrawler.kbqa.parse import SPARQL_SELECT_STMT, SPARQL_PREFIX


def request(query: str, endpoint="http://localhost:3030/kg/sparql") -> tuple:
    """发送 SPARQL 查询请求"""
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["head"]["vars"], [(v['value'] for k, v in d.items()) for d in results["results"]["bindings"]]


def get_name(name_, id_):
    exp = f"""
        ?s rdf:type :{name_[3:]}.
        ?s :{name_[3:]}_id {id_}.
        ?s :{name_[3:]}_name ?name. """
    stmt = SPARQL_SELECT_STMT.format(
        prefix=SPARQL_PREFIX,
        select='?name',
        expression=exp,
    )
    # print(stmt)
    res = request(stmt)[1]
    for r in res:
        return [r_ for r_ in r][-1]
    return res


def key_mapping(d: dict) -> dict:
    def _map(k: str, v: str) -> tuple:
        k_ = k.split('#')[-1]
        if not k_:
            return None, None
        v_ = v
        if 'file' in v:
            n_ = v.split('#')[-1]
            n_, id_ = n_.split('/')
            v_ = get_name(n_, id_)

        return KEY_MAPPING.get(k_), v_

    res = {}
    for k, v in d.items():
        k_, v_ = _map(k, v)
        if k_ and v_:
            if k_ not in res:
                res[k_] = [v_]
            else:
                res[k_].append(v_)
    return {k: v if len(v) != 1 else v[-1] for k, v in res.items()}


def res_format(vars_: list, bindings_: list) -> dict:
    """
    将 bindings 转为可读的 json 格式
    :param vars_:
    :param bindings_:
    :return:
    """
    bindings_ = [list(v) for v in bindings_]
    if not vars_:
        return key_mapping({'answer': "我不知道"})
    elif len(vars_) == 1:
        return key_mapping({vars_[0]: ','.join([v[0] for v in bindings_])})
    else:
        bindings_ = bindings_[:]
        # print(bindings_)
        # TODO: multiple value
        mapped = key_mapping({v[-2]: v[-1] for v in bindings_})
        return mapped
