import allure

from mall_tiny_test.common.db_util import query_all


def query_user_resource(username, resource_url):
    sql = """
        select
            a.username,
            r.name as role_name,
            res.url
        from ums_admin a
        join ums_admin_role_relation ar on a.id = ar.admin_id
        join ums_role r on ar.role_id = r.id
        join ums_role_resource_relation rr on r.id = rr.role_id
        join ums_resource res on rr.resource_id = res.id
        where a.username = %s
          and res.url = %s
    """

    return query_all(sql, (username, resource_url))


@allure.feature("权限关系")
@allure.story("超级管理员拥有后台用户列表权限")
def test_admin_access_admin_list_permission(admin_token):
    result = query_user_resource("admin", "/admin/**")

    assert len(result) > 0, "未查询到 admin 用户的权限信息"


@allure.feature("权限关系")
@allure.story("商品管理员没有后台用户列表权限")
def test_product_admin_access_admin_list_permission():
    result = query_user_resource("productAdmin", "/admin/**")

    assert len(result) == 0, "查询到 productAdmin 用户的权限信息，预期没有权限"


@allure.feature("权限关系")
@allure.story("订单管理员没有后台用户列表权限")
def test_order_admin_access_admin_list_permission():
    result = query_user_resource("orderAdmin", "/admin/**")

    assert len(result) == 0, "查询到 orderAdmin 用户的权限信息，预期没有权限"
