from refo import Star, Any, finditer

from medscrawler.kbqa.parse import QuestionSet
from medscrawler.kbqa.words import Words


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


rules = [
    Rule(
        condition_num=2,
        condition=Words.WORD_DISEASE + Star(Any(), greedy=False) + Words.WORD_MEDICINE + Star(Any(), greedy=False),
        action=QuestionSet.medicine_for_disease,
    ),
]
