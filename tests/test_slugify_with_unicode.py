from test_common import *

from mooseblog.slugify import django_slugify, faker_slugify

UNICODE_ENABLED = True


def test_slugify_kha_with_unicode():
    # Test to verify that kha remains, in roman character
    expected_result_with_unicode = "х"
    actual_result = django_slugify(input_str_kha, allow_unicode=UNICODE_ENABLED)
    assert actual_result == expected_result_with_unicode

    unicode_actual_result_faker = faker_slugify(input_str_kha, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result_faker == expected_result_with_unicode


def test_slugify_ve_with_unicode():
    # Test to verify that ve remains, in roman character

    unicode_actual_result = django_slugify(input_str_ve, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result == "в"

    unicode_actual_result_faker = faker_slugify(input_str_ve, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result_faker == "в"


def test_slugify_russian():
    expected_result_with_unicode = "текст-на-русском"

    unicode_actual_result = django_slugify(inpurt_str_text_in_russian, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result == expected_result_with_unicode

    unicode_actual_result_faker = faker_slugify(inpurt_str_text_in_russian, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result_faker == expected_result_with_unicode


def test_slugify_spanish():
    expected_result_with_unicode = "una-lágrima-cayó-en-la-arena"

    unicode_actual_result = django_slugify(input_str_text_in_spanish, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result == expected_result_with_unicode

    unicode_actual_result = faker_slugify(input_str_text_in_spanish, allow_unicode=UNICODE_ENABLED)
    assert unicode_actual_result == expected_result_with_unicode
