from collections import namedtuple

import jieba as _jieba
from jieba.posseg import cut as _cut

Word = namedtuple('Word', ['token', 'pos'])


def load_userdict(dict_path: str):
    _jieba.load_userdict(dict_path)


def suggest_freq(segment: tuple, tune: bool = True):
    _jieba.suggest_freq(segment, tune)


def parse(sentence: str) -> list:
    return [Word(word, tag) for word, tag in _cut(sentence)]


load_userdict("./meds_dict.txt")
