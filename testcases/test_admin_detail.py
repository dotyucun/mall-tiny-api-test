import allure

from common.request_util import send_request, assert_status_code
from common.db_util import query_one


@allure.feature("后台用户管理")
@allure.story("根据 ID 获取后台用户信息")
def test_get_admin_by_id_success(admin_token, admin_factory):
    created_admin = admin_factory()
    admin_id = created_admin["id"]
    username = created_admin["payload"]["username"]

    response = send_request(
        "GET",
        f"/admin/{admin_id}",
        token=admin_token,
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 200
    assert body["message"] == "操作成功"
    assert body["data"] is not None
    assert body["data"]["id"] == admin_id
    assert body["data"]["username"] == username

    db_admin = query_one(
        "select id, username from ums_admin where id = %s",
        (admin_id,),
    )

    assert db_admin is not None
    assert body["data"]["id"] == db_admin["id"]
    assert body["data"]["username"] == db_admin["username"]
