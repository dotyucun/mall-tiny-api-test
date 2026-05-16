import os
import yaml
import requests


CURRENT_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(CURRENT_DIR, "..", "config", "config.yaml")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

BASE_URL = config["base_url"].rstrip("/")
TIMEOUT = config["timeout"]


def send_requests(method, path, token=None, **kwargs):
    """
    mall-tiny 接口请求封装。

    method: 请求方法，例如 GET / POST
    path: 接口路径，例如 /admin/login
    token: 完整 token，例如 Bearer xxxxx
    kwargs: requests 支持的参数，例如 json、params、headers
    """
    url = BASE_URL + path
    headers = kwargs.pop("headers", {}).copy()

    if token:
        headers["Authorization"] = token

    return requests.request(
        method=method,
        url=url,
        headers=headers,
        timeout=TIMEOUT,
        **kwargs,
    )


def send_request(method, path, token=None, **kwargs):
    return send_requests(method, path, token=token, **kwargs)


def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, (
        f"请求失败，状态码：{response.status_code}，响应内容：{response.text}"
    )


def assert_field_not_empty(body, field_name):
    assert field_name in body and body[field_name] not in (None, "", [], {}), (
        f"字段 {field_name} 为空或不存在，body={body}"
    )
