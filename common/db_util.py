import pymysql

from mall_tiny_test.common.yaml_util import load_yaml


config = load_yaml("config/config.yaml")
mysql_config = config["mysql"]


def get_connection():
    return pymysql.connect(
        host=mysql_config["host"],
        port=mysql_config["port"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )


def query_one(sql, params=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    finally:
        connection.close()


def query_all(sql, params=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        connection.close()


def execute(sql, params=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            affected_rows = cursor.execute(sql, params)
        connection.commit()
        return affected_rows
    finally:
        connection.close()
