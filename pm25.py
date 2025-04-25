import pandas as pd
import pymysql


def open_db():
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost", port=3306, user="root", password="12345678", db="demo"
        )
    except Exception as e:
        print("The Data open erro ......")
    return conn


def get_pm25_data_from_mysql():
    datas = None
    conn = None
    columns = None
    try:
        conn = open_db()
        cur = conn.cursor()
        # sqlstr = "(select MAX(datacreationdate) from pm25;)"

        sqlstr = "select * from pm25 where datacreationdate=(select MAX(datacreationdate) from pm25);"
        cur.execute(sqlstr)
        print(cur.description)
        columns = [col[0] for col in cur.description]
        datas = cur.fetchall()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
    return datas, columns


if __name__ == "__main__":
    datas, columns = get_pm25_data_from_mysql()
    print(columns)
