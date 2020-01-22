import MySQLdb
import datetime

from db import DBConnector
from model.project import project

class innerList:
    """ユーザーモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              # id int notNull
        self.attr["user_id"] = None       # 冷蔵庫id
        self.attr["product_name"] = None    # 品名
        self.attr["lim"] = None           # 賞味期限
        self.attr["amount"] = None          # 個数
        self.attr["whose"] = None           # 誰のものか
        self.attr["kind"] = None           # 分類

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_innerList;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_innerList` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `user_id` int(11) unsigned NOT NULL,
                    `product_name` varchar(255) DEFAULT NULL,
                    `lim` varchar(255) DEFAULT NULL,
                    `amount` varchar(255) DEFAULT NULL,
                    `whose` varchar(255) DEFAULT NULL,
                    `kind` varchar(255) DEFAULT NULL,
                    PRIMARY KEY (`id`)
                ); """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP IF EXISTS DATABASE db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_innerList
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        i = innerList()
        i.attr["id"] = data["id"]
        i.attr["user_id"] = data["user_id"]
        i.attr["product_name"] = data["product_name"]
        i.attr["lim"] = data["lim"]
        i.attr["amount"] = data["amount"]
        i.attr["whose"] = data["whose"]
        i.attr["kind"] = data["kind"]
        return i

    @staticmethod
    def build():
        i = innerList()
        return i

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
          self.attr["product_name"] is not None and type(self.attr["product_name"]) is str,
          self.attr["lim"] is not None and type(self.attr["lim"]) is str,
          self.attr["amount"] is not None and type(self.attr["amount"]) is str,
          self.attr["whose"] is not None and type(self.attr["whose"]) is str,
          self.attr["kind"] is not None and type(self.attr["kind"]) is str,
        ])

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["id"] == None:
            return self._db_save_insert()
        return self._db_save_update()

    def _db_save_insert(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_innerList
                    (user_id, product_name, lim, amount, whose, kind)
                VALUES
                    (%s, %s, %s, %s, %s, %s); """,
                (self.attr["user_id"],
                self.attr["product_name"],
                self.attr["lim"],
                self.attr["amount"],
                self.attr["whose"],
                self.attr["kind"]))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_innerList
                SET user_id = %s,
                    product_name = %s,
                    lim = %s,
                    amount = %s,
                    whose = %s,
                    kind = %s
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["product_name"],
                self.attr["lim"],
                self.attr["amount"],
                self.attr["whose"],
                self.attr["kind"],
                self.attr["id"]))

            con.commit()

        return self.attr["id"]

    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_innerList
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()

        records = []
        for data in results:
            il = innerList()
            il.attr["id"] = data["id"]
            il.attr["user_id"] = data["user_id"]
            il.attr["product_name"] = data["product_name"]
            il.attr["lim"] = data["lim"]
            il.attr["amount"] = data["amount"]
            il.attr["whose"] = data["whose"]
            il.attr["kind"] = data["kind"]
            records.append(il)

        return records

    def delete(self):
        if self.attr["id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_innerList
                WHERE id = %s; """,
                (self.attr["id"],))
            con.commit()

            return self.attr["id"]

    @staticmethod
    def search(user_id,word):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM table_innerList WHERE product_name LIKE '{}%' OR whose LIKE '{}%' OR kind LIKE '{}%' AND user_id = {}".format(word,word,word,user_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            results = cursor.fetchall()

        records = []
        for data in results:
            il = innerList()
            il.attr["id"] = data["id"]
            il.attr["user_id"] = data["user_id"]
            il.attr["product_name"] = data["product_name"]
            il.attr["lim"] = data["lim"]
            il.attr["amount"] = data["amount"]
            il.attr["whose"] = data["whose"]
            il.attr["kind"] = data["kind"]
            records.append(il)

        return records
