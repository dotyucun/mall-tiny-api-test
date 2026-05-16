import allure
import pytest

from common.request_util import send_request, assert_status_code
from common.yaml_util import load_yaml


config = load_yaml("config/config.yaml")
login_failed_cases = load_yaml("data/login_data.yaml")["login_failed_cases"]


@allure.feature("后台用户管理")
@allure.story("登录成功场景")
def test_admin_login_success():
    admin = config["accounts"]["admin"]

    response = send_request(
        "POST",
        "/admin/login",
        json={
            "username": admin["username"],
            "password": admin["password"],
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 200
    assert body["message"] == "操作成功"
    assert body["data"]["token"] is not None, "登录成功但未返回 token"
    assert body["data"]["tokenHead"] == "Bearer ", "登录成功但 tokenHead 不正确"


@allure.feature("后台用户管理")
@allure.story("登录失败场景")
@pytest.mark.parametrize("case", login_failed_cases, ids=lambda case: case["case_name"])
def test_admin_login_fail(case):
    response = send_request(
        "POST",
        "/admin/login",
        json={
            "username": case["username"],
            "password": case["password"],
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == case["expected_code"], (
        f"登录失败但响应 code 不正确，响应内容：{body}"
    )
    assert body["message"] == case["expected_message"], (
        f"登录失败但响应 message 不正确，响应内容：{body}"
    )
    assert body["data"] is None, f"登录失败但响应 data 不为 None，响应内容：{body}"


@allure.feature("后台用户管理")
@allure.story("不同后台账号登录成功")
@pytest.mark.parametrize("account_key", ["admin", "product_admin", "order_admin"])
def test_admin_accounts_login_success(account_key):
    account = config["accounts"][account_key]

    response = send_request(
        "POST",
        "/admin/login",
        json={
            "username": account["username"],
            "password": account["password"],
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 200
    assert body["message"] == "操作成功"
    assert body["data"] is not None
    assert body["data"]["token"] is not None
    assert body["data"]["tokenHead"] == "Bearer "
