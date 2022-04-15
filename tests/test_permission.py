from mooseblog.models import ArticleModel, FileModel, ImageModel
from mooseblog.permission import Permission, UserModel


def test_john_has_image_permission():
    """Verify John can access Images."""
    all_permissions = Permission()
    requested_access = ImageModel.schema()
    assert all_permissions.has_permission(
        UserModel(username="John"), requested_access
    )


def test_paul_doesnt_have_image_permission():
    """Verify Paul can't access Images."""
    all_permissions = Permission()
    requested_access = ImageModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Paul"), requested_access
    )


def test_ringo_doesnt_have_image_permission():
    """Verify Ringo can't access Images or Files."""
    all_permissions = Permission()
    requested_access = ImageModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Ringo"), requested_access
    )
    requested_access = FileModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Ringo"), requested_access
    )


def test_george_doesnt_have_image_permission():
    """Verify George can access Articles and Images, but not Files."""
    all_permissions = Permission()
    requested_access = ArticleModel.schema()
    assert all_permissions.has_permission(
        UserModel(username="George"), requested_access
    )
    requested_access = ImageModel.schema()
    assert all_permissions.has_permission(
        UserModel(username="George"), requested_access
    )
    requested_access = FileModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="George"), requested_access
    )


def test_john_has_multiple_permissions_in_one_call():
    """Verify John has multiple permissions in single call."""
    all_permissions = Permission()
    requested_access = [
        ArticleModel.schema(),
        ImageModel.schema(),
        FileModel.schema(),
    ]
    response = all_permissions.has_permission(
        UserModel(username="John"), requested_access
    )
    assert response is True


def test_peter_has_no_permission():
    """Verify Peter has no authorization."""
    all_permissions = Permission()
    requested_access = ArticleModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Peter"), requested_access
    )
    requested_access = ImageModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Peter"), requested_access
    )
    requested_access = FileModel.schema()
    assert not all_permissions.has_permission(
        UserModel(username="Peter"), requested_access
    )
