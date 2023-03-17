from pydantic import BaseModel

from mooseapi.models import ArticleModel, FileModel, ImageModel

"""
This module is a fake permission system, dealing only with authorization
and not authentication.

Note: This is NOT a robust security design, it is only meant for 
discussion.  To secure this FastAPI application, follow the 
tutorial: https://fastapi.tiangolo.com/tutorial/security/
"""


class UserModel(BaseModel):
    """
    This model represents an authenticated users in the system.

    Note: Since Pydantic's BaseModel isn't hashable by default,
    we've added our own __hash__ definition to support using this
    model as a dictionary's key (see Permission class).
    """

    username: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class Permission:
    """
    This model represents a cache of authorized data access (sub-types of BaseModel) for a given
    person (UserModel).
    """

    def __init__(self) -> None:
        # The permissions model depends on the schema of the data requested.  This is
        # a nice feature, since if the data model changes or if the client attempts
        # to ask for permission with an invalid schema, the authorization will be denied.
        self.app_permissions = {
            UserModel(username="John"): [
                ArticleModel.schema(),
                FileModel.schema(),
                ImageModel.schema(),
            ],
            UserModel(username="Paul"): [
                ArticleModel.schema(),
                FileModel.schema(),
            ],
            UserModel(username="Ringo"): [ArticleModel.schema()],
            UserModel(username="George"): [
                ArticleModel.schema(),
                ImageModel.schema(),
            ],
        }

    def has_permission(self, user: UserModel, permission_requested) -> bool:
        """
        Check if 'user' is authorized to access the 'permission_requested'.
        """
        authorize_access = False
        if user in self.app_permissions:
            # Look at specific model
            user_access = self.app_permissions[user]
            if isinstance(permission_requested, list):
                authorize_access = all(
                    permission_req in user_access
                    for permission_req in permission_requested
                )
            elif isinstance(permission_requested, dict):
                authorize_access = permission_requested in user_access
            else:
                print("Warning: Invalid permission_requested")

        return authorize_access
