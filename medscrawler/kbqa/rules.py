from refo import Star, Any, finditer

from medscrawler.kbqa.parse import QuestionSet
from medscrawler.kbqa.words import Words


class Rule:
    def __init__(self, condition_num, condition, action):
        self.condition_num = condition_num
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


rules = [
    Rule(
        condition_num=1,
        condition=Words.WORD_DISEASE + Words.WORD_IS + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.disease_info,
    ),
    Rule(
        condition_num=1,
        condition=Words.WORD_MEDICINE + Words.WORD_IS + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.medicine_info,
    ),
    Rule(
        condition_num=1,
        condition=Words.WORD_DISEASE + Star(Any(), greedy=False) + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.medicine_for_disease,
    ),
    Rule(
        condition_num=2,
        condition=Words.WORD_DISEASE + Star(Any(), greedy=False) + Words.WORD_OF + Star(Any(), greedy=False) +
                  Words.WORD_SPEC + Star(Any(), greedy=False),
        action=QuestionSet.disease_spec,
    ),
]
