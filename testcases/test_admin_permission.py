import allure

from mall_tiny_test.common.request_util import send_request, assert_status_code


@allure.feature("后台用户管理")
@allure.story("商品管理员无权限访问后台用户列表")
def test_product_admin_get_admin_list_no_permission(product_admin_token):
    response = send_request(
        "GET",
        "/admin/list",
        token=product_admin_token,
        params={
            "pageNum": 1,
            "pageSize": 5,
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 403
    assert body["message"] == "没有相关权限"
    assert body["data"] == "抱歉，您没有访问权限"


@allure.feature("后台用户管理")
@allure.story("订单管理员无权限访问后台用户列表")
def test_order_admin_get_admin_list_no_permission(order_admin_token):
    response = send_request(
        "GET",
        "/admin/list",
        token=order_admin_token,
        params={
            "pageNum": 1,
            "pageSize": 5,
        },
    )

    assert_status_code(response, 200)
    body = response.json()

    assert body["code"] == 403
    assert body["message"] == "没有相关权限"
    assert body["data"] == "抱歉，您没有访问权限"
