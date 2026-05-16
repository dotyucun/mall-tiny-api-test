import allure

from common.request_util import send_request, assert_status_code


@allure.feature("后台用户管理")
@allure.story("获取管理员信息")
def test_get_admin_info(admin_token):
    response = send_request(
        "GET",
        "/admin/info",
        token=admin_token,
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 200, f"获取管理员信息失败，响应内容：{body}"
    assert body["message"] == "操作成功"
    assert body["data"] is not None, "获取管理员信息失败，响应 data 为空"
    assert "roles" in body["data"], "管理员信息中缺少 roles 字段"
    assert "超级管理员" in body["data"]["roles"], "管理员角色不正确，期望包含超级管理员"


@allure.feature("后台用户管理")
@allure.story("未登录获取管理员信息")
def test_get_admin_info_unauthorized():
    response = send_request(
        "GET",
        "/admin/info",
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 401
    assert body["message"] == "暂未登录或token已经过期"
    assert body["data"] is None
