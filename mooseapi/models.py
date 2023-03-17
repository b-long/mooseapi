import inspect
import json
from enum import Enum
from typing import Type

from fastapi import Form
from pydantic import BaseModel

"""
Collection of Pydantic models, for use in FastAPI application.

Pydantic is a nice option, as it provides built-in IDE support
in VSCode, Pycharm, and other IDEs.

More info: 
    https://pydantic-docs.helpmanual.io/

Use in FastAPI:
    https://fastapi.tiangolo.com/tutorial/body/
    https://fastapi.tiangolo.com/tutorial/body-nested-models/
"""


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints.

    Note, this is a workaround due to https://github.com/tiangolo/fastapi/issues/2387 .

    Without it, we're unable to write an endpoint which consumes
    a file and structured (typed) data simultaneously as form-data.
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
            annotation=field.outer_type_,
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


@as_form
class ArticleModel(BaseModel):
    # Note, we don't use "name" becuase it effects Form-Data usage
    article_name: str
    # Note: If 'slug' is missing, the application will generate one using the name
    slug: str = None
    content: str


class FileModel(BaseModel):
    name: str
    binary_content: bytes
    article: ArticleModel

    def __str__(self) -> str:
        # Stringify nicely, without bytes
        r = {k: self.dict()[k] for k in ("name", "article")}
        return json.dumps(r)


class ImageType(str, Enum):
    JPEG = "jpeg"
    PNG = "png"


class ImageModel(FileModel):
    """
    The 'ImageModel' type extends the 'FileModel', and adds a "type" property.

    The type can be either 'jpg' or 'png' (see the 'ImageType' enum)
    """

    type: ImageType
