import pytest

from mall_tiny_test.common.request_util import send_request
from mall_tiny_test.common.yaml_util import load_yaml


config = load_yaml("config/config.yaml")


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


@pytest.fixture(scope="session")
def admin_token():
    return get_token("admin")


@pytest.fixture(scope="session")
def product_admin_token():
    return get_token("product_admin")


@pytest.fixture(scope="session")
def order_admin_token():
    return get_token("order_admin")