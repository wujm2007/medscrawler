import hug

from medscrawler.kbqa.parse import get_sparql
from medscrawler.utils.sparql import request, res_format


@hug.get('/query')
def query(q: hug.types.text) -> dict:
    """
    通过自然语言进行 SPARQL 查询，
    :param q: 自然语言问题
    :return: 可读的 JSON 格式数据
    """
    sparql = get_sparql(q)
    if not sparql:
        res = [], []
    else:
        res = request(sparql, endpoint="http://localhost:3030/kg/sparql")
    return res_format(*res)


@hug.static('/static')
def my_static_dirs():
    return 'static',
