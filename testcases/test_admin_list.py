import allure

from mall_tiny_test.common.request_util import send_request, assert_status_code
from mall_tiny_test.common.yaml_util import load_yaml


admin_data = load_yaml("data/admin_data.yaml")
admin_list_data = admin_data["admin_list_data"]


@allure.feature("后台用户管理")
@allure.story("获取后台用户列表")
def test_get_admin_list(admin_token):
    response = send_request(
        "GET",
        "/admin/list",
        token=admin_token,
        params={
            "pageNum": admin_list_data["page_num"],
            "pageSize": admin_list_data["page_size"],
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == admin_list_data["expected_code"]
    assert body["message"] == admin_list_data["expected_message"]
    assert body["data"] is not None
    assert "list" in body["data"]
    assert isinstance(body["data"]["list"], list)
