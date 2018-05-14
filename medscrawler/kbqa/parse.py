from config import DEBUG
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
                ?o :cure_disease_id ?s.
                ?o :cure_medicine_id ?m.
                ?m :medicine_name_cn ?medicine_name_cn. """.format(w.token)

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
