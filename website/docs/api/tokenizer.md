---
title: Tokenizer
teaser: Segment text into words, punctuations marks etc.
tag: class
source: spacy/tokenizer.pyx
---

Segment text, and create `Doc` objects with the discovered segment boundaries.

## Tokenizer.\_\_init\_\_ {#init tag="method"}

Create a `Tokenizer`, to create `Doc` objects given unicode text.

> #### Example
>
> ```python
> # Construction 1
> from spacy.tokenizer import Tokenizer
> tokenizer = Tokenizer(nlp.vocab)
>
> # Construction 2
> from spacy.lang.en import English
> tokenizer = English().Defaults.create_tokenizer(nlp)
> ```

| Name             | Type        | Description                                                                         |
| ---------------- | ----------- | ----------------------------------------------------------------------------------- |
| `vocab`          | `Vocab`     | A storage container for lexical types.                                              |
| `rules`          | dict        | Exceptions and special-cases for the tokenizer.                                     |
| `prefix_search`  | callable    | A function matching the signature of `re.compile(string).search` to match prefixes. |
| `suffix_search`  | callable    | A function matching the signature of `re.compile(string).search` to match suffixes. |
| `infix_finditer` | callable    | A function matching the signature of `re.compile(string).finditer` to find infixes. |
| `token_match`    | callable    | A boolean function matching strings to be recognized as tokens.                     |
| **RETURNS**      | `Tokenizer` | The newly constructed object.                                                       |

## Tokenizer.\_\_call\_\_ {#call tag="method"}

Tokenize a string.

> #### Example
>
> ```python
> tokens = tokenizer(u"This is a sentence")
> assert len(tokens) == 4
> ```

| Name        | Type    | Description                             |
| ----------- | ------- | --------------------------------------- |
| `string`    | unicode | The string to tokenize.                 |
| **RETURNS** | `Doc`   | A container for linguistic annotations. |

## Tokenizer.pipe {#pipe tag="method"}

Tokenize a stream of texts.

> #### Example
>
> ```python
> texts = [u"One document.", u"...", u"Lots of documents"]
> for doc in tokenizer.pipe(texts, batch_size=50):
>     pass
> ```

| Name         | Type  | Description                                              |
| ------------ | ----- | -------------------------------------------------------- |
| `texts`      | -     | A sequence of unicode texts.                             |
| `batch_size` | int   | The number of texts to accumulate in an internal buffer. |
| **YIELDS**   | `Doc` | A sequence of Doc objects, in order.                     |

## Tokenizer.find_infix {#find_infix tag="method"}

Find internal split points of the string.

| Name        | Type    | Description                                                                                                                                        |
| ----------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `string`    | unicode | The string to split.                                                                                                                               |
| **RETURNS** | list    | A list of `re.MatchObject` objects that have `.start()` and `.end()` methods, denoting the placement of internal segment separators, e.g. hyphens. |

## Tokenizer.find_prefix {#find_prefix tag="method"}

Find the length of a prefix that should be segmented from the string, or `None`
if no prefix rules match.

| Name        | Type    | Description                                            |
| ----------- | ------- | ------------------------------------------------------ |
| `string`    | unicode | The string to segment.                                 |
| **RETURNS** | int     | The length of the prefix if present, otherwise `None`. |

## Tokenizer.find_suffix {#find_suffix tag="method"}

Find the length of a suffix that should be segmented from the string, or `None`
if no suffix rules match.

| Name        | Type         | Description                                            |
| ----------- | ------------ | ------------------------------------------------------ |
| `string`    | unicode      | The string to segment.                                 |
| **RETURNS** | int / `None` | The length of the suffix if present, otherwise `None`. |

## Tokenizer.add_special_case {#add_special_case tag="method"}

Add a special-case tokenization rule. This mechanism is also used to add custom
tokenizer exceptions to the language data. See the usage guide on
[adding languages](/usage/adding-languages#tokenizer-exceptions) for more
details and examples.

> #### Example
>
> ```python
> from spacy.attrs import ORTH, LEMMA
> case = [{"don't": [{ORTH: "do"}, {ORTH: "n't", LEMMA: "not"}]}]
> tokenizer.add_special_case(case)
> ```

| Name          | Type     | Description                                                                                                                                                              |
| ------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `string`      | unicode  | The string to specially tokenize.                                                                                                                                        |
| `token_attrs` | iterable | A sequence of dicts, where each dict describes a token and its attributes. The `ORTH` fields of the attributes must exactly match the string when they are concatenated. |

## Attributes {#attributes}

| Name             | Type    | Description                                                                                                                |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| `vocab`          | `Vocab` | The vocab object of the parent `Doc`.                                                                                      |
| `prefix_search`  | -       | A function to find segment boundaries from the start of a string. Returns the length of the segment, or `None`.            |
| `suffix_search`  | -       | A function to find segment boundaries from the end of a string. Returns the length of the segment, or `None`.              |
| `infix_finditer` | -       | A function to find internal segment separators, e.g. hyphens. Returns a (possibly empty) list of `re.MatchObject` objects. |