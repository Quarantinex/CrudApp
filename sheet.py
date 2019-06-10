
import pymysql



connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='crud',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()


