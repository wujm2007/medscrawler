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
    # 【疾病】是什么？
    Rule(
        condition_num=1,
        condition=Words.WORD_DISEASE + Words.WORD_IS + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.disease_info,
    ),
    # 【药品】是什么？
    Rule(
        condition_num=1,
        condition=Words.WORD_MEDICINE + Words.WORD_IS + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.medicine_info,
    ),
    # 【疾病】怎么办？
    Rule(
        condition_num=1,
        condition=Words.WORD_DISEASE + Star(Any(), greedy=False) + Words.WORD_ASK + Star(Any(), greedy=False),
        action=QuestionSet.medicine_for_disease,
    ),
    # 【疾病】的【特性】是什么？
    Rule(
        condition_num=2,
        condition=Words.WORD_DISEASE + Star(Any(), greedy=False) + Words.WORD_OF + Star(Any(), greedy=False) +
                  Words.WORD_SPEC + Star(Any(), greedy=False),
        action=QuestionSet.disease_spec,
    ),
]
