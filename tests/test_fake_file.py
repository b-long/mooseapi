import csv
from pathlib import Path
from typing import Tuple

from faker import Faker

from mooseblog.conf import output_dir
from tests.test_common import fake_file_csv_rows_to_generate

"""
A module to generate fake files.
"""


def generate_fake_file() -> Tuple[Path, str]:
    """
    Generate a fake Markdown file.

    TODO: Re-work generation of content-type
    """
    fake = Faker()
    fake_file = output_dir / "test_data.csv"
    content_type = "text/markdown"

    with open(fake_file, "w", newline="") as csvfile:
        fieldnames = ["author_email", "article"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _ in range(fake_file_csv_rows_to_generate):
            writer.writerow(
                {
                    "author_email": fake.email(),
                    # For information about generating fake articles, see:
                    # https://faker.readthedocs.io/en/master/providers/faker.providers.lorem.html#faker.providers.lorem.Provider.paragraph
                    "article": fake.paragraph(nb_sentences=7),
                }
            )
    return fake_file, content_type
