import pymysql
from config import Config
import os

def connect_db():
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset=Config.MYSQL_CHARSET
    )
    return connection

def init_db():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r', encoding='utf-8') as f:
                sql = f.read()
                for statement in sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement)
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    init_db()