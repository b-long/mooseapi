from pathlib import Path
from typing import Tuple

from faker import Faker
from pydantic import validate_arguments

from mooseblog.conf import output_dir
from mooseblog.models import ImageType

"""
A module to generate fake images.
"""


def generate_fake_image(
    image_type: ImageType, output_file_name: Path
) -> Tuple[Path, str]:
    """
    Generate a fake image file.

    TODO: Re-work generation of content-type
    """
    fake = Faker()
    Faker.seed(0)
    content_type = f"image/{image_type.value}"

    output_file_name.parent.mkdir(parents=True, exist_ok=True)
    data = fake.image(
        size=(200, 200),
        hue="blue",
        luminosity="bright",
        image_format=image_type.value,
    )

    with open(output_file_name, "wb") as f:
        f.write(data)

    return output_file_name, content_type


@validate_arguments
def generate_fake_image_series(format: ImageType):
    """
    Generate blue sample image (200 x 200 pixels) in given format, e.g. 'jpeg' or 'png'.

    For more information about using Faker's image provider, see:
    https://faker.readthedocs.io/en/master/providers/faker.providers.misc.html#faker.providers.misc.Provider.image
    """
    for i in range(5):
        generate_fake_image(
            format, output_dir / f"test_{format}_image_{i}.{format}"
        )


if __name__ == "__main__":
    generate_fake_image_series(format=ImageType.JPEG)
    generate_fake_image_series(format=ImageType.PNG)
    # generate_fake_image_series(format="foo")
