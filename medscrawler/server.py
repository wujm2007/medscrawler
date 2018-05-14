import hug

from medscrawler.kbqa.parse import get_sparql
from medscrawler.utils.sparql import request, res_format


@hug.get('/query')
def query(query: hug.types.text) -> dict:
    sparql = get_sparql(query)
    if not sparql:
        res = [], []
    else:
        res = request(sparql, endpoint="http://localhost:3030/med_kg/query")
    return res_format(*res)


@hug.static('/static')
def my_static_dirs():
    return 'static',
