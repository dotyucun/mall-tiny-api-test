import uuid

import allure

from mall_tiny_test.common.db_util import execute, query_one
from mall_tiny_test.common.request_util import send_request, assert_status_code
from mall_tiny_test.common.yaml_util import load_yaml


admin_data = load_yaml("data/admin_data.yaml")
admin_crud_data = admin_data["admin_crud"]


def build_admin_payload():
    suffix = uuid.uuid4().hex[:10]
    username = f"{admin_crud_data['username_prefix']}{suffix}"

    return {
        "username": username,
        "password": admin_crud_data["password"],
        "email": f"{username}@{admin_crud_data['email_domain']}",
        "nickName": admin_crud_data["created_nick_name"],
        "note": admin_crud_data["created_note"],
    }


def cleanup_admin(admin_id=None, username=None):
    if admin_id:
        execute("delete from ums_admin_role_relation where admin_id = %s", (admin_id,))
        execute("delete from ums_admin_login_log where admin_id = %s", (admin_id,))
        execute("delete from ums_admin where id = %s", (admin_id,))

    if username:
        execute("delete from ums_admin where username = %s", (username,))


def create_admin(admin_token):
    payload = build_admin_payload()
    admin_id = None

    cleanup_admin(username=payload["username"])

    response = send_request(
        "POST",
        "/admin/register",
        token=admin_token,
        json=payload,
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 200
    assert body["message"] == "操作成功"
    assert body["data"] is not None
    assert body["data"]["id"] is not None
    assert body["data"]["username"] == payload["username"]

    admin_id = body["data"]["id"]
    return admin_id, payload


@allure.feature("后台用户管理")
@allure.story("创建后台用户并校验数据库")
def test_create_admin_success_with_db_assert(admin_token):
    admin_id = None
    payload = None

    try:
        admin_id, payload = create_admin(admin_token)

        db_admin = query_one(
            "select id, username, email, nick_name, note, status from ums_admin where id = %s",
            (admin_id,),
        )

        assert db_admin is not None
        assert db_admin["username"] == payload["username"]
        assert db_admin["email"] == payload["email"]
        assert db_admin["nick_name"] == payload["nickName"]
        assert db_admin["note"] == payload["note"]
        assert db_admin["status"] == 1
    finally:
        if payload:
            cleanup_admin(admin_id=admin_id, username=payload["username"])


@allure.feature("后台用户管理")
@allure.story("修改后台用户并禁用账号")
def test_update_admin_success_with_db_assert(admin_token):
    admin_id = None
    payload = None

    try:
        admin_id, payload = create_admin(admin_token)
        updated_email = f"updated_{payload['email']}"
        update_payload = {
            "username": payload["username"],
            "email": updated_email,
            "nickName": admin_crud_data["updated_nick_name"],
            "note": admin_crud_data["updated_note"],
            "status": 1,
        }

        update_response = send_request(
            "POST",
            f"/admin/update/{admin_id}",
            token=admin_token,
            json=update_payload,
        )

        assert_status_code(update_response, 200)
        update_body = update_response.json()
        assert update_body["code"] == 200
        assert update_body["message"] == "操作成功"

        status_response = send_request(
            "POST",
            f"/admin/updateStatus/{admin_id}",
            token=admin_token,
            params={"status": 0},
        )

        assert_status_code(status_response, 200)
        status_body = status_response.json()
        assert status_body["code"] == 200
        assert status_body["message"] == "操作成功"

        db_admin = query_one(
            "select username, email, nick_name, note, status from ums_admin where id = %s",
            (admin_id,),
        )

        assert db_admin is not None
        assert db_admin["username"] == payload["username"]
        assert db_admin["email"] == updated_email
        assert db_admin["nick_name"] == update_payload["nickName"]
        assert db_admin["note"] == update_payload["note"]
        assert db_admin["status"] == 0
    finally:
        if payload:
            cleanup_admin(admin_id=admin_id, username=payload["username"])


@allure.feature("后台用户管理")
@allure.story("删除后台用户并校验数据库")
def test_delete_admin_success_with_db_assert(admin_token):
    admin_id = None
    payload = None

    try:
        admin_id, payload = create_admin(admin_token)

        response = send_request(
            "POST",
            f"/admin/delete/{admin_id}",
            token=admin_token,
        )

        assert_status_code(response, 200)
        body = response.json()

        assert body["code"] == 200
        assert body["message"] == "操作成功"

        db_admin = query_one(
            "select id from ums_admin where id = %s",
            (admin_id,),
        )

        assert db_admin is None
    finally:
        if payload:
            cleanup_admin(admin_id=admin_id, username=payload["username"])
