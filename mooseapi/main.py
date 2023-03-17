from fastapi import Depends, FastAPI, Form, UploadFile
from fastapi.params import File

from mooseapi.image_processing import decode_image
from mooseapi.models import ArticleModel, FileModel, ImageModel, ImageType
from mooseapi.slugify import faker_slugify

"""
Basic FastAPI application.
"""
app = FastAPI()


@app.post("/upload-file")
async def upload_file(
    new_file_name: str = Form(...),
    parent_article: ArticleModel = Depends(ArticleModel.as_form),
    new_file: UploadFile = File(...),
):
    """
    Endpoint to create (POST) a new File, with special handling
    for JPEG and PNG images.

    Note, this endpoint is a bit atypical, since it requires both
    form data and an upload file.
    """
    # Get bytes like object
    file_content_bytes = new_file.file.read()

    response = {
        "request-received": True,
        "content_type": new_file.content_type,
        "name": new_file_name,
    }

    # pylint: disable=E1101,W0212
    if (
        new_file.content_type.replace("image/", "").upper()
        in ImageType._member_names_
    ):
        print("Processing image type file")
        file = ImageModel(
            name=new_file_name,
            binary_content=file_content_bytes,
            article=parent_article,
            type=ImageType(new_file.content_type.replace("image/", "")),
        )
        # Some additional detail to distinguish the response
        image = decode_image(file_content_bytes)
        dimensions = {"height": image.height, "width": image.width}
        response["dimensions"] = dimensions
    else:
        print("Processing non-image type file")
        file = FileModel(
            name=new_file_name,
            binary_content=file_content_bytes,
            article=parent_article,
        )

    response["article"] = parent_article
    print(f"Created new file '{file}'")

    return response


@app.post("/articles")
async def create_article(article: ArticleModel):
    """
    Endpoint to create (POST) a new Article, automatically creates a slug and returns the JSON model.
    """
    item_dict = article.dict()
    if article.slug is None:
        item_dict.update({"slug": faker_slugify(article.article_name)})

    return item_dict
