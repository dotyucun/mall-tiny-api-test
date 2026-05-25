import allure

from common.db_util import query_one
from common.request_util import send_request, assert_status_code
from common.yaml_util import load_yaml


admin_data = load_yaml("data/admin_data.yaml")
admin_test_data = admin_data["temporary_admin"]


@allure.feature("后台用户管理")
@allure.story("创建后台用户并校验数据库")
def test_create_admin_success_with_db_assert(admin_factory):
    created_admin = admin_factory()
    payload = created_admin["payload"]

    db_admin = query_one(
        "select id, username, email, nick_name, note, status from ums_admin where id = %s",
        (created_admin["id"],),
    )

    assert db_admin is not None
    assert db_admin["username"] == payload["username"]
    assert db_admin["email"] == payload["email"]
    assert db_admin["nick_name"] == payload["nickName"]
    assert db_admin["note"] == payload["note"]
    assert db_admin["status"] == 1


@allure.feature("后台用户管理")
@allure.story("修改后台用户并禁用账号")
def test_update_admin_success_with_db_assert(admin_token, admin_factory):
    created_admin = admin_factory()
    admin_id = created_admin["id"]
    payload = created_admin["payload"]
    updated_email = f"updated_{payload['email']}"
    update_payload = {
        "username": payload["username"],
        "email": updated_email,
        "nickName": admin_test_data["updated_nick_name"],
        "note": admin_test_data["updated_note"],
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


@allure.feature("后台用户管理")
@allure.story("删除后台用户并校验数据库")
def test_delete_admin_success_with_db_assert(admin_token, admin_factory):
    created_admin = admin_factory()
    admin_id = created_admin["id"]

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
