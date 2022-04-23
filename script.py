from mysql.connector import connect, Error

try:
    with connect(
        host='mysql.osinvladislav.myjino.ru',
        user='046502789_aloe',
        password='aloevera') as connection:
        print(connection)
except Error as e:
    print(e)
