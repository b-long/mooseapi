"""
The process of creating a "slug", often called a "slugify" function, is
non-trivial.  The challenge is in supporting unicode strings AND making 
the result user-friendly.

For example, what if your goal is to help someone with an en-US keyboard 
type non-Roman characters?

Instead of re-inventing the wheel, this module borrows from other
packages.  It is probably best to invoke the functions discussed 
here, or to migrate to a package specifically created for this purpose
like: 
 - https://github.com/un33k/python-slugify
 - https://github.com/avian2/unidecode

Discussions on GitHub and StackOverflow provide some test cases:

    Format
    ------
    Expect:
        "X Slug"
    To be:
        "x-slug"

    Examples
    --------
    Expect: 
        "Una lágrima cayó en la arena"
    To be:
        "una-lagrima-cayo-en-la-arena"

    Expect:
        "Текст на русском"
    To be:
        "текст-на-русском"

The 'Faker' package that we depend on, already has a 'slugify'
function, and we've have copied it here for discussion.  

Source:
- https://github.com/joke2k/faker/blob/v8.14.0/faker/utils/text.py        

The 'Django' package (which isn't used in this project), already
has a 'slugify' function, and we've have copied it here for discussion.

Source:
    https://github.com/django/django/blob/3.2.7/django/utils/text.py#L398-L411
"""

import re
import unicodedata

_re_pattern = re.compile(r"[^\w\s-]", flags=re.U)
_re_pattern_allow_dots = re.compile(r"[^\.\w\s-]", flags=re.U)
_re_spaces = re.compile(r"[-\s]+", flags=re.U)


def faker_slugify(
    value: str, allow_dots: bool = False, allow_unicode: bool = False
) -> str:
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace. Modified to optionally allow dots.

    Adapted from Django 1.9
    """
    if allow_dots:
        pattern = _re_pattern_allow_dots
    else:
        pattern = _re_pattern

    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
        value = pattern.sub("", value).strip().lower()
        return _re_spaces.sub("-", value)
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    value = pattern.sub("", value).strip().lower()
    return _re_spaces.sub("-", value)


def django_slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def flet_slugify(original: str) -> str:
    """
    Source:
    https://github.com/flet-dev/flet/blob/7fabc35c62812b3cca99672dd9ae2fde3bc8b84b/sdk/python/flet/utils.py#L113-L134

    Originally merged to Flet:
    https://github.com/flet-dev/flet/pull/154

    Note: this implementation preserves unicode characters.

    Make a string url friendly. Useful for creating routes for navigation.
    >>> slugify("What's    up?")
    'whats-up'

    # Finnish "How are you?"
    >>> slugify("  Mitä kuuluu?  ")
    'mitä-kuuluu'
    """
    slugified = original.strip()
    slugified = " ".join(slugified.split())  # Remove extra spaces between words
    slugified = slugified.lower()
    """
    About unicodedata.category(), returns a category like below:
    * Lu (letter uppercase)
    * Ll (letter lowercase)
    * Po (punctuation other)

    >>> print(unicodedata.category(u'A'))
    Lu
    >>> print(unicodedata.category(u'b'))
    Ll
    >>> print(unicodedata.category(u'?'))
    Po

    More info: 
    https://www.askpython.com/python-modules/unicode-in-python-unicodedata
    """
    # Remove unicode punctuation
    slugified = "".join(
        character
        for character in slugified
        if not unicodedata.category(character).startswith("P")
    )
    return slugified.replace(" ", "-")
