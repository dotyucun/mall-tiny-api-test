import allure

from mall_tiny_test.common.request_util import send_request, assert_status_code


@allure.feature("后台用户管理")
@allure.story("无 token 获取后台用户列表")
def test_get_admin_list_no_token():
    response = send_request(
        "GET",
        "/admin/list",
        params={
            "pageNum": 1,
            "pageSize": 5,
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 401
    assert body["message"] == "暂未登录或token已经过期"
    assert "authentication" in body["data"]
