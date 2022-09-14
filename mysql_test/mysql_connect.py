import pymysql
# import charts


# 資料庫設定
db_settings = {
    "host": "192.168.12.87",
    "port": 3306,
    "user": "Sony",
    "password": "Sony_SN2489",
    "db": "Sony_SN_Manager",
    "charset": "utf8"
}


try:
    # 建立Connection物件
    conn = pymysql.connect(**db_settings)
    # 建立Cursor物件
    with conn.cursor() as cursor:
        # 查詢資料SQL語法
        command = "SELECT * FROM Sony_SN"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        print(result)

    # with conn.cursor() as cursor:
    # #資料表相關操作
    # print("hello")

except Exception as ex:
    print(ex)