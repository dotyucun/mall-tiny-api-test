import uuid

import pytest

from common.db_util import execute, query_one
from common.request_util import send_request
from common.yaml_util import load_yaml


config = load_yaml("config/config.yaml")
admin_test_data = load_yaml("data/admin_data.yaml")["temporary_admin"]


def get_token(account_key):
    account = config["accounts"][account_key]

    response = send_request(
        "POST",
        "/admin/login",
        json={
            "username": account["username"],
            "password": account["password"]
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["code"] == 200
    assert body["data"] is not None
    assert body["data"]["token"] is not None
    assert body["data"]["tokenHead"] == "Bearer "

    return body["data"]["tokenHead"] + body["data"]["token"]


def cleanup_admin(admin_id, username):
    if admin_id is None:
        admin = query_one("select id from ums_admin where username = %s", (username,))
        admin_id = admin["id"] if admin else None

    if admin_id is None:
        return

    execute("delete from ums_admin_role_relation where admin_id = %s", (admin_id,))
    execute("delete from ums_admin_login_log where admin_id = %s", (admin_id,))
    execute("delete from ums_admin where id = %s", (admin_id,))


@pytest.fixture(scope="session")
def admin_token():
    return get_token("admin")


@pytest.fixture(scope="session")
def product_admin_token():
    return get_token("product_admin")


@pytest.fixture(scope="session")
def order_admin_token():
    return get_token("order_admin")


@pytest.fixture
def admin_factory(admin_token):
    created_admins = []

    def create_admin():
        suffix = uuid.uuid4().hex[:10]
        username = f"{admin_test_data['username_prefix']}{suffix}"
        payload = {
            "username": username,
            "password": admin_test_data["password"],
            "email": f"{username}@{admin_test_data['email_domain']}",
            "nickName": admin_test_data["created_nick_name"],
            "note": admin_test_data["created_note"],
        }

        response = send_request(
            "POST",
            "/admin/register",
            token=admin_token,
            json=payload,
        )

        assert response.status_code == 200
        body = response.json()
        body_data = body.get("data") if isinstance(body, dict) else None
        created_admin = {
            "id": body_data.get("id") if isinstance(body_data, dict) else None,
            "payload": payload,
        }
        created_admins.append(created_admin)

        assert body["code"] == 200
        assert body["message"] == "操作成功"
        assert body["data"] is not None
        assert body["data"]["id"] is not None
        assert body["data"]["username"] == username

        return created_admin

    yield create_admin

    for admin in reversed(created_admins):
        cleanup_admin(admin["id"], admin["payload"]["username"])
