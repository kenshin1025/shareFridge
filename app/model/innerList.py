import MySQLdb
import datetime

from db import DBConnector
from model.project import project

class innerList:
    """ユーザーモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              # id int notNull
        self.attr["fridge_id"] = None       # 冷蔵庫id
        self.attr["product_name"] = None    # 品名
        self.attr["lim"] = None           # 賞味期限
        self.attr["amount"] = None          # 個数
        self.attr["whose"] = None           # 誰のものか
        self.attr["class"] = None           # 分類

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
                    `fridge_id` int(11) unsigned NOT NULL,
                    `product_name` varchar(255) DEFAULT NULL,
                    `lim` int(11) NOT NULL,
                    `amount` decimal(12,0) NOT NULL DEFAULT '0',
                    `whose` varchar(255) DEFAULT NULL,
                    `class` varchar(255) DEFAULT NULL,
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
        i.attr["fridge_id"] = data["fridge_id"]
        i.attr["product_name"] = data["product_name"]
        i.attr["lim"] = data["lim"]
        i.attr["amount"] = data["amount"]
        i.attr["whose"] = data["whose"]
        i.attr["class"] = data["class"]
        return i

    @staticmethod
    def build():
        i = innerList()
        return i

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["fridge_id"] is not None and type(self.attr["fridge_id"]) is int,
          self.attr["product_name"] is not None and type(self.attr["product_name"]) is str,
          self.attr["lim"] is not None and type(self.attr["lim"]) is int,
          self.attr["amount"] is not None and type(self.attr["amount"]) is int,
          self.attr["whose"] is not None and type(self.attr["whose"]) is str,
          self.attr["class"] is not None and type(self.attr["class"]) is str,
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
                    (fridge_id, product_name, lim, amount, whose, class)
                VALUES
                    (%s, %s, %s, %s, %s, %s); """,
                (self.attr["fridge_id"],
                self.attr["product_name"],
                self.attr["lim"],
                self.attr["amount"],
                self.attr["whose"],
                self.attr["class"]))

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
                SET fridge_id = %s,
                    product_name = %s,
                    lim = %s,
                    amount = %s,
                    whose = %s,
                    class = %s
                WHERE id = %s; """,
                (self.attr["fridge_id"],
                self.attr["product_name"],
                self.attr["lim"],
                self.attr["amount"],
                self.attr["whose"],
                self.attr["class"],
                self.attr["id"]))

            con.commit()

        return self.attr["id"]

    @staticmethod
    def select_by_fridge_id(fridge_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_innerList
                WHERE  fridge_id = %s;
            """, (fridge_id,))
            results = cursor.fetchall()

        records = []
        for data in results:
            f = fridge()
            f.attr["id"] = data["id"]
            f.attr["fridge_id"] = data["fridge_id"]
            f.attr["product_name"] = data["product_name"]
            f.attr["lim"] = data["lim"]
            f.attr["amount"] = data["amount"]
            f.attr["whose"] = data["whose"]
            f.attr["class"] = data["class"]
            records.append(f)

        return records