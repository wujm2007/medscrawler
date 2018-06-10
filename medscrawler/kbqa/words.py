import re

from refo import Predicate

from medscrawler.const import KEY_MAPPING_INV


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
    POS_DISEASE = "n"
    POS_MEDICINE = "nz"


class Words:
    WORD_DISEASE = W(pos=Positions.POS_DISEASE)
    WORD_MEDICINE = W(pos=Positions.POS_MEDICINE)
    specs = list(KEY_MAPPING_INV.keys())
    WORD_SPEC = W(specs[0])
    for spec in specs[1:]:
        WORD_SPEC = WORD_SPEC | W(spec)
    WORD_ASK = (W("怎么办") | W("怎么") | W('什么') | W('啥'))
    WORD_OF = (W("的"))
    WORD_IS = W("是")
