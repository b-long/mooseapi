from fastapi.testclient import TestClient

from mooseblog.conf import output_dir
from mooseblog.main import app
from mooseblog.models import ArticleModel, ImageType
from tests.test_fake_file import generate_fake_file
from tests.test_fake_images import generate_fake_image

client = TestClient(app)

TEST_ARTICLE_NAME = (
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
)
TEST_CONTENT = (
    "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took"
    " a galley of type and scrambled it to make a type specimen book."
)
TEST_SLUG = (
    "lorem-ipsum-is-simply-dummy-text-of-the-printing-and-typesetting-industry"
)
BASIC_ARTICLE_DICT = {
    "article_name": TEST_ARTICLE_NAME,
    "content": TEST_CONTENT,
    "slug": TEST_SLUG,
}


def test_create_article_lorem_ipsum_en():
    art = ArticleModel(
        article_name="Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        content=(
            "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took"
            " a galley of type and scrambled it to make a type specimen book."
        ),
    )

    body = art.json()

    response = client.post(
        "/articles",
        body,
    )

    assert response.status_code == 200
    assert response.json() == BASIC_ARTICLE_DICT


def test_create_article_lorem_ipsum_cs():
    art = ArticleModel(
        article_name="Lorem Ipsum je demonstrativní výplňový text používaný v tiskařském a knihařském průmyslu.",
        content=(
            "Lorem Ipsum je považováno za standard v této oblasti už od začátku 16. století, kdy dnes neznámý tiskař"
            " vzal kusy textu a na jejich základě vytvořil speciální vzorovou knihu. Jeho odkaz nevydržel pouze pět"
            " století, on přežil i nástup elektronické sazby v podstatě beze změny."
        ),
    )

    body = art.json()

    response = client.post(
        "/articles",
        body,
    )

    assert response.status_code == 200
    assert response.json() == {
        "article_name": "Lorem Ipsum je demonstrativní výplňový text používaný v tiskařském a knihařském průmyslu.",
        "content": (
            "Lorem Ipsum je považováno za standard v této oblasti už od začátku 16. století, kdy dnes neznámý tiskař"
            " vzal kusy textu a na jejich základě vytvořil speciální vzorovou knihu. Jeho odkaz nevydržel pouze pět"
            " století, on přežil i nástup elektronické sazby v podstatě beze změny."
        ),
        "slug": "lorem-ipsum-je-demonstrativni-vyplnovy-text-pouzivany-v-tiskarskem-a-kniharskem-prumyslu",
    }


def test_upload_image():
    filename, content_type = generate_fake_image(
        ImageType.JPEG, output_dir / f"test_upload_image.{ImageType.JPEG}"
    )

    form_data = BASIC_ARTICLE_DICT.copy()
    form_data["new_file_name"] = filename

    with open(file=filename, mode="rb") as f:
        response = client.post(
            "/upload-file",
            data=form_data,
            files={
                "new_file": (
                    "filename",
                    f,
                    content_type,
                )
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "request-received": True,
        "content_type": "image/jpeg",
        "name": str(filename),
        "dimensions": {"height": 200, "width": 200},
        "article": {
            "article_name": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            "slug": "lorem-ipsum-is-simply-dummy-text-of-the-printing-and-typesetting-industry",
            "content": (
                "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer"
                " took a galley of type and scrambled it to make a type specimen book."
            ),
        },
    }


def test_upload_file():
    filename, content_type = generate_fake_file()

    form_data = BASIC_ARTICLE_DICT.copy()
    form_data["new_file_name"] = filename

    with open(file=filename, mode="rb") as f:
        response = client.post(
            "/upload-file",
            data=form_data,
            files={
                "new_file": (
                    "filename",
                    f,
                    content_type,
                )
            },
        )

    assert response.status_code == 200
    assert response.json() == {
        "request-received": True,
        "content_type": "text/markdown",
        "name": str(filename),
        "article": {
            "article_name": "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            "slug": "lorem-ipsum-is-simply-dummy-text-of-the-printing-and-typesetting-industry",
            "content": (
                "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer"
                " took a galley of type and scrambled it to make a type specimen book."
            ),
        },
    }
