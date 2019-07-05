# encoding: utf8
from __future__ import unicode_literals, print_function

import re
import sys


from .stop_words import STOP_WORDS
from .tag_map import TAG_MAP, POS
from ...attrs import LANG
from ...language import Language
from ...tokens import Doc
from ...compat import copy_reg
from ...util import DummyTokenizer
from ...compat import is_python3, is_python_pre_3_5

is_python_post_3_7 = is_python3 and sys.version_info[1] >= 7

# fmt: off
if is_python_pre_3_5:
    from collections import namedtuple
    Morpheme = namedtuple("Morpheme", "surface lemma tag")
elif is_python_post_3_7:
    from dataclasses import dataclass
    @dataclass(frozen=True)
    class Morpheme:
        surface: str
        lemma: str
        tag: str
else:
    from typing import NamedTuple
    class Morpheme(NamedTuple):
        surface: str
        lemma: str
        tag: str


def try_mecab_import():
    try:
        from natto import MeCab
        return MeCab
    except ImportError:
        raise ImportError(
            "Korean support requires [mecab-ko](https://bitbucket.org/eunjeon/mecab-ko/src/master/README.md), "
            "[mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic), "
            "and [natto-py](https://github.com/buruzaemon/natto-py)"
        )
# fmt: on


def check_spaces(text, tokens):
    token_pattern = re.compile(r"\s?".join(f"({t})" for t in tokens))
    m = token_pattern.match(text)
    if m is not None:
        for i in range(1, m.lastindex):
            yield m.end(i) < m.start(i + 1)
        yield False


class KoreanTokenizer(DummyTokenizer):
    def __init__(self, cls, nlp=None):
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.Tokenizer = try_mecab_import()

    def __call__(self, text):
        dtokens = list(self.detailed_tokens(text))
        surfaces = [dt.surface for dt in dtokens]
        doc = Doc(self.vocab, words=surfaces, spaces=list(check_spaces(text, surfaces)))
        for token, dtoken in zip(doc, dtokens):
            first_tag, sep, eomi_tags = dtoken.tag.partition("+")
            token.tag_ = first_tag  # stem(어간) or pre-final(선어말 어미)
            token.lemma_ = dtoken.lemma
        doc.user_data["full_tags"] = [dt.tag for dt in dtokens]
        return doc

    def detailed_tokens(self, text):
        with self.Tokenizer() as tokenizer:
            for node in tokenizer.parse(text, as_nodes=True):
                if node.is_eos():
                    break
                surface = node.surface
                feature = node.feature
                # 품사 태그, 의미 부류,	종성 유무, 읽기, 타입, 첫번째 품사,	마지막 품사, 표현, *
                (
                    pos,
                    sem_class,
                    reading,
                    type_,
                    start_pos,
                    end_pos,
                    expr,
                    _,
                ) = feature.split(",")
                tag = pos
                lemma, sep, remainder = expr.partition("/")
                if lemma == "*":
                    lemma = surface
                yield Morpheme(surface, lemma, tag)


class KoreanDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda _text: "ko"
    stop_words = STOP_WORDS
    tag_map = TAG_MAP
    writing_system = {"direction": "ltr", "has_case": False, "has_letters": False}

    @classmethod
    def create_tokenizer(cls, nlp=None):
        return KoreanTokenizer(cls, nlp)


class Korean(Language):
    lang = "ko"
    Defaults = KoreanDefaults

    def make_doc(self, text):
        return self.tokenizer(text)


def pickle_korean(instance):
    return Korean, tuple()


copy_reg.pickle(Korean, pickle_korean)

__all__ = ["Korean"]