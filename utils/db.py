import pymysql
from tablib import Dataset

mysql_config = {
    "user": "bookmark",
    "password": "bookmark@123",
    "database": "bookmark"
}


def query_dataset(cursor, stmt, *args, **kwargs) -> Dataset:
    cursor.execute(stmt, args)
    table_name = kwargs.get("table_name", "")
    dataset = Dataset(title=table_name)
    dataset.headers = (desc[0] for desc in cursor.description)
    for row in cursor:
        dataset.append(row)
    return dataset


def insert_dataset(cursor, dataset, **kwargs):
    table_name = kwargs.get("table_name")
    if not table_name:
        table_name = dataset.title

    if not table_name:
        raise Exception("请传入关键字参数table_name")

    fields = ",".join(field for field in dataset.headers)
    place_holders = ",".join("%s" for _ in dataset.headers)
    sql = "insert into %s(%s) values (%s)" % (table_name, fields, place_holders)
    cursor.executemany(sql, dataset[:])


def save(dataset, **kwargs):
    with pymysql.connect(**mysql_config) as cursor:
        insert_dataset(cursor, dataset, **kwargs)


def query(stmt, *args, **kwargs):
    with pymysql.connect(**mysql_config) as cursor:
        return query_dataset(cursor, stmt, *args, **kwargs)