import allure

from common.request_util import send_request, assert_status_code
from common.yaml_util import load_yaml
from common.db_util import query_one


admin_data = load_yaml("data/admin_data.yaml")
admin_detail_data = admin_data["admin_detail"]


@allure.feature("后台用户管理")
@allure.story("根据 ID 获取后台用户信息")
def test_get_admin_by_id_success(admin_token):
    admin_id = admin_detail_data["admin_id"]

    response = send_request(
        "GET",
        f"/admin/{admin_id}",
        token=admin_token,
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == admin_detail_data["expected_code"]
    assert body["message"] == admin_detail_data["expected_message"]
    assert body["data"] is not None
    assert body["data"]["id"] == admin_id
    assert body["data"]["username"] == admin_detail_data["expected_username"]

    db_admin = query_one(
        "select id, username from ums_admin where id = %s",
        (admin_id,),
    )

    assert db_admin is not None
    assert body["data"]["id"] == db_admin["id"]
    assert body["data"]["username"] == db_admin["username"]
