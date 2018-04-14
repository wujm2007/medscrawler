from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper(endpoint="http://localhost:3030/med_kg/query")
sparql.setQuery("""
    PREFIX : <http://www.medicine-kg.com#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?n WHERE {
      ?s rdf:type :disease.
      ?s :disease_infectious True.
      ?o :cure_disease_id ?s.
      ?o :cure_medicine_id ?m.
      ?m :medicine_name_cn ?n.
    }
    LIMIT 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for binding in results["results"]["bindings"]:
    print(
        "\t".join("{}: {}".format(k, v['value']) for k, v in binding.items())
    )
