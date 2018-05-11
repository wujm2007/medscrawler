from SPARQLWrapper import SPARQLWrapper, JSON

from medscrawler.kbqa.parse import get_sparql

sparql = SPARQLWrapper(endpoint="http://localhost:3030/kg/sparql")
sparql.setQuery(get_sparql('青光眼吃什么药'))
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for binding in results["results"]["bindings"]:
    print(
        "\t".join("{}: {}".format(k, v['value']) for k, v in binding.items())
    )
