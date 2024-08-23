# import sys
# import os
#
# import pymysql
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#
# from db.db_connection import db_connect
# from db.migrations.rides_migration import create_rides_table
# from db.migrations.books_migration import create_books_table
#
# def main():
#     commands = (
#         create_rides_table(),
#         create_books_table()
#     )
#
#     conn = None
#     try:
#         conn = db_connect()
#         cur = conn.cursor()
#
#         for command in commands:
#             cur.execute(command)
#
#         cur.close()
#         conn.commit()
#         print("Tables created successfully.")
#
#     except (Exception, pymysql.MySQLError) as error:
#         print(f"Error: {error}")
#     finally:
#         if conn is not None:
#             conn.close()
#
#
# if __name__ == "__main__":
#     main()
