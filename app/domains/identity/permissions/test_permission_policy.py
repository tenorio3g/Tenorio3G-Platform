from app.domains.identity.permissions import (
    PermissionPolicy,
)


def test_admin_should_manage_users():

    assert PermissionPolicy.has_permission(
        "ADMIN",
        "users.manage",
    ) is True


def test_technician_should_view_assets():

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "assets.view",
    ) is True


def test_technician_should_not_manage_users():

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "users.manage",
    ) is False


def test_supervisor_should_manage_people():

    assert PermissionPolicy.has_permission(
        "SUPERVISOR",
        "people.manage",
    ) is True


def test_manager_should_not_manage_roles():

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "roles.manage",
    ) is False


def test_unknown_role_should_have_no_permissions():

    assert PermissionPolicy.has_permission(
        "UNKNOWN",
        "assets.view",
    ) is False


def test_should_normalize_role_and_permission():

    assert PermissionPolicy.has_permission(
        " admin ",
        " USERS.MANAGE ",
    ) is True


def test_permissions_for_should_return_role_permissions():

    permissions = (
        PermissionPolicy.permissions_for(
            "TECHNICIAN"
        )
    )

    assert "assets.view" in permissions
    assert "users.manage" not in permissions

def test_admin_should_manage_documents():

    assert PermissionPolicy.has_permission(
        "ADMIN",
        "documents.manage",
    ) is True


def test_manager_should_view_documents_but_not_manage_them():

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "documents.view",
    ) is True

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "documents.manage",
    ) is False


def test_supervisor_should_manage_photos():

    assert PermissionPolicy.has_permission(
        "SUPERVISOR",
        "photos.manage",
    ) is True


def test_technician_should_view_photos():

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "photos.view",
    ) is True


def test_technician_should_manage_maintenance():

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "maintenance.manage",
    ) is True


def test_manager_should_view_maintenance_but_not_manage_it():

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "maintenance.view",
    ) is True

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "maintenance.manage",
    ) is False

def test_admin_should_manage_preventive_maintenance():

    assert PermissionPolicy.has_permission(
        "ADMIN",
        "preventive.manage",
    ) is True


def test_supervisor_should_manage_preventive_maintenance():

    assert PermissionPolicy.has_permission(
        "SUPERVISOR",
        "preventive.manage",
    ) is True


def test_manager_should_view_but_not_manage_preventive_maintenance():

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "preventive.view",
    ) is True

    assert PermissionPolicy.has_permission(
        "MANAGER",
        "preventive.manage",
    ) is False


def test_technician_should_view_but_not_manage_preventive_maintenance():

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "preventive.view",
    ) is True

    assert PermissionPolicy.has_permission(
        "TECHNICIAN",
        "preventive.manage",
    ) is False