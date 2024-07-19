import mysql.connector
from mysql.connector import Error

def get_database():
    conn = None
    conn = mysql.connector.connect(
        host='database-1.cpugetver0n9.us-east-1.rds.amazonaws.com',
        database='ridio',  # 新しいデータベース名
        user='admin',
        password='software6'  # パスワードを入力
    )
    return conn