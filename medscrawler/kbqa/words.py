import re

from refo import Predicate


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        super().__init__(self.match)
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Positions:
    POS_DISEASE = "nr"
    POS_MEDICINE = "v"


class Words:
    WORD_DISEASE = W(pos=Positions.POS_DISEASE)
    WORD_MEDICINE = W(pos=Positions.POS_MEDICINE)
    MEDICINE = W("药")
