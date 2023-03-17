from test_common import (
    input_str_kha,
    inpurt_str_text_in_russian,
    input_str_text_in_spanish,
    input_str_ve,
)

from mooseapi.slugify import django_slugify, faker_slugify

UNICODE_ENABLED = False


def test_slugify_kha_without_unicode():
    # Test to verify that kha is removed
    expected_result_without_unicode = ""
    actual_result = django_slugify(input_str_kha, allow_unicode=UNICODE_ENABLED)
    assert actual_result == expected_result_without_unicode

    non_unicode_actual_result_faker = faker_slugify(
        input_str_kha, allow_unicode=UNICODE_ENABLED
    )
    assert actual_result == non_unicode_actual_result_faker


def test_slugify_ve_without_unicode():
    # Test to verify that ve is removed
    unicode_actual_result = django_slugify(
        input_str_ve, allow_unicode=UNICODE_ENABLED
    )
    assert unicode_actual_result == ""

    non_unicode_actual_result = django_slugify(
        input_str_ve, allow_unicode=UNICODE_ENABLED
    )
    assert non_unicode_actual_result == ""


def test_slugify_russian():
    expected_result_without_unicode = ""

    unicode_actual_result = django_slugify(
        inpurt_str_text_in_russian, allow_unicode=UNICODE_ENABLED
    )
    assert unicode_actual_result == expected_result_without_unicode

    unicode_actual_result_faker = faker_slugify(
        inpurt_str_text_in_russian, allow_unicode=UNICODE_ENABLED
    )
    assert unicode_actual_result_faker == expected_result_without_unicode


def test_slugify_spanish():
    expected_result_without_unicode = "una-lagrima-cayo-en-la-arena"

    unicode_actual_result = django_slugify(
        input_str_text_in_spanish, allow_unicode=UNICODE_ENABLED
    )
    assert unicode_actual_result == expected_result_without_unicode

    unicode_actual_result = faker_slugify(
        input_str_text_in_spanish, allow_unicode=UNICODE_ENABLED
    )
    assert unicode_actual_result == expected_result_without_unicode
