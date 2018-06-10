from config import DEBUG
from medscrawler.const import KEY_MAPPING_INV
from medscrawler.kbqa import parse
from medscrawler.kbqa.words import Positions

SPARQL_PREFIX = """PREFIX : <http://www.medicine-kg.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"""

SPARQL_SELECT_STMT = """{prefix}\n
SELECT DISTINCT {select} WHERE {{{expression}
}}"""

SPARQL_COUNT_STMT = """{prefix}\n
SELECT COUNT({select}) WHERE {{{expression}
}}"""

SPARQL_ASK_STMT = """{prefix}\n
ASK {{{expression}
}}\n"""


class QuestionSet:
    @staticmethod
    def medicine_for_disease(word_objects):
        select = "?medicine_name_cn"

        for w in word_objects:
            if w.pos == Positions.POS_DISEASE:
                e = """
                ?s rdf:type :disease.
                ?s :disease_name_cn '{}'.
                ?s :cured ?o.
                ?o :medicine_name_cn ?medicine_name_cn. """.format(w.token)

                sparql = SPARQL_SELECT_STMT.format(
                    prefix=SPARQL_PREFIX,
                    select=select,
                    expression=e,
                )
                return sparql
        return

    @staticmethod
    def medicine_info(word_objects):
        select = "?s ?p ?o"

        for w in word_objects:
            if w.pos == Positions.POS_MEDICINE:
                e = """
                ?s rdf:type :medicine.
                ?s :medicine_name_cn '{}'.
                ?s ?p ?o. """.format(w.token)

                sparql = SPARQL_SELECT_STMT.format(
                    prefix=SPARQL_PREFIX,
                    select=select,
                    expression=e,
                )
                return sparql
        return

    @staticmethod
    def disease_info(word_objects):
        select = "?s ?p ?o"

        for w in word_objects:
            if w.pos == Positions.POS_DISEASE:
                e = """
                ?s rdf:type :disease.
                ?s :disease_name_cn '{}'.
                ?s ?p ?o. """.format(w.token)

                sparql = SPARQL_SELECT_STMT.format(
                    prefix=SPARQL_PREFIX,
                    select=select,
                    expression=e,
                )
                return sparql
        return

    @staticmethod
    def disease_spec(word_objects):
        select = "?s ?p ?o"

        disease_name, spec = None, None

        e = """
                         ?s rdf:type :disease.
                         ?s :disease_name_cn '{}'.
                         ?s :{} ?o. """
        for w in word_objects:
            if w.pos == Positions.POS_DISEASE and not disease_name:
                disease_name = w.token
            elif w.pos == Positions.POS_DISEASE:
                spec = w.token
        if disease_name and spec:
            sparql = SPARQL_SELECT_STMT.format(
                prefix=SPARQL_PREFIX,
                select=select.format(KEY_MAPPING_INV.get(spec, 'unknown')),
                expression="""
                ?s rdf:type :disease.
                ?s :disease_name_cn '{}'.
                ?s :{} ?o. 
                ?s ?p ?o.""".format(disease_name, KEY_MAPPING_INV.get(spec, 'unknown'))
            )
            return sparql


def get_sparql(question: str) -> str:
    word_objects = parse(question)

    if DEBUG:
        for word in word_objects:
            print(word)

    result_q, matches = None, -1

    from medscrawler.kbqa.rules import rules

    for rule in rules:
        query, num = rule.apply(word_objects)

        if query is not None and num > matches:
            result_q, matches = query, num

    return result_q
