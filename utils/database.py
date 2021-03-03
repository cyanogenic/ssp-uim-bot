import mysql.connector
from config import DataBaseConfig

DBCONFIG = DataBaseConfig

class MyDB():
    def __init__(self ,             \
        host =   DBCONFIG.HOST,     \
        port =   DBCONFIG.PORT,     \
        username=DBCONFIG.USERNAME, \
        password=DBCONFIG.PASSWD,   \
        database=DBCONFIG.DATABASE, \
    ):
        '''类例化，处理一些连接操作'''
        self.host     = host
        self.username = username
        self.password = password
        self.database = database
        self.port     = port
        self.cur      = None
        self.con      = None
        # connect to mysql
        try:
            self.con = mysql.connector.connect(host = self.host, user = self.username, password = self.password, port = self.port, database = self.database)
            self.cur = self.con.cursor()
            print("======== 数据库连接初始化成功 ========")
        except :
            raise "DataBase connect error,please check the db config."

    def close(self):
        '''结束查询和关闭连接'''
        self.con.close()
        print("======== 数据库连接关闭成功 ========")

    def create_table(self,sql_str):
        '''创建数据表'''
        try:
            self.cur.execute(sql_str)
        except Exception as e:
            print(e)
    def query_formatrs(self,sql_str):
        '''查询数据，返回一个列表，里面的每一行是一个字典，带字段名
             cursor 为连接光标
             sql_str为查询语句
        '''
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            r = []
            for x in rows:
                r.append(dict(zip(self.cur.column_names,x)))

            return r
        except:
            return False

    def query(self,sql_str):
        '''查询数据并返回
            cursor 为连接光标
            sql_str为查询语句
        '''
        try:

            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            return rows
        except:
            return False

    def execute_update_insert(self,sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.lastrowid
