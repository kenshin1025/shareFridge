import MySQLdb
import datetime

from db import DBConnector
from model.project import project

class wishList:
    """欲しいものリストモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              # id int notNull
        self.attr["user_id"] = None       # user_id int notNull
        self.attr["name"] = None            # name str notNull
        self.attr["quantity"] = None          # quantity str notNull
        self.attr["kind"] = None           # kind str notNull
        self.attr["last_updated"] = None    # last_updated date notNull

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_wishList;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_wishList` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `user_id` int(11) unsigned NOT NULL,
                    `name` varchar(255) DEFAULT NULL,
                    `quantity` varchar(255) DEFAULT NULL,
                    `kind` varchar(255) DEFAULT NULL,
                    `last_updated` datetime NOT NULL,
                    PRIMARY KEY (`id`),
                    KEY `user_id` (`user_id`)
                )""")
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_wishList
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        w = wishList()
        w.attr["id"] = data["id"]
        w.attr["user_id"] = data["user_id"]
        w.attr["name"] = data["name"]
        w.attr["quantity"] = data["quantity"]
        w.attr["kind"] = data["kind"]
        w.attr["last_updated"] = data["last_updated"]
        return w

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["user_id"] is not None and type(self.attr["user_id"]) is int,
          self.attr["name"] is None or type(self.attr["name"]) is str,
          self.attr["quantity"] is not None and type(self.attr["quantity"]) is str,
          self.attr["kind"] is not None and type(self.attr["kind"]) is str,
          self.attr["last_updated"] is not None and type(self.attr["last_updated"]) is datetime.datetime
        ])

    @staticmethod
    def build():
        now = datetime.datetime.now()
        w = wishList()
        w.attr["last_updated"] = now
        return w

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
                INSERT INTO table_wishList
                    (user_id, name, quantity, kind, last_updated)
                VALUES
                    (%s, %s, %s, %s, %s); """,
                (self.attr["user_id"],
                self.attr["name"],
                self.attr["quantity"],
                self.attr["kind"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"])))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_wishList
                SET user_id = %s,
                    name = %s,
                    quantity = %s,
                    kind = %s,
                    last_updated = %s
                WHERE id = %s; """,
                (self.attr["user_id"],
                self.attr["name"],
                self.attr["quantity"],
                self.attr["kind"],
                '{0:%Y-%m-%d %H:%M:%S}'.format(self.attr["last_updated"]),
                self.attr["id"]))

            con.commit()

        return self.attr["id"]

    @staticmethod
    def select_by_user_id(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_wishList
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()

        records = []
        for data in results:
            w = wishList()
            w.attr["id"] = data["id"]
            w.attr["user_id"] = data["user_id"]
            w.attr["name"] = data["name"]
            w.attr["quantity"] = data["quantity"]
            w.attr["kind"] = data["kind"]
            w.attr["last_updated"] = data["last_updated"]
            records.append(w)

        return records

    # 指定したidのデータ取り出しデータベースから削除する関数
    @staticmethod
    def move(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_wishList
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

            if (len(results) == 0):
                return None
            data = results[0]
            w = wishList()
            w.attr["id"] = data["id"]
            w.attr["user_id"] = data["user_id"]
            w.attr["name"] = data["name"]
            w.attr["quantity"] = data["quantity"]
            w.attr["kind"] = data["kind"]
            w.attr["last_updated"] = data["last_updated"]

            # データの削除(DELETE)
            cursor.execute("""
                DELETE
                FROM table_wishList
                WHERE id = %s; """,
                (id,)
                )
            con.commit()

        return w

    def delete(self):
        if self.attr["id"] == None: return None
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_wishList
                WHERE id = %s; """,
                (self.attr["id"],))
            con.commit()
        return self.attr["id"]

    @staticmethod
    def name(user_id, name):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM table_wishList
                WHERE user_id = %s and name = %s
                ORDER BY `quantity` ASC; """,
                (user_id,name,))
            con.commit()
            recodes = cursor.fetchall()

        w_list = [wishList.find(recode[0]) for recode in recodes]
        return w_list

    @staticmethod
    def kind(user_id, kind):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT id FROM table_wishList
                WHERE user_id = %s and kind = %s
                ORDER BY `quantity` ASC; """,
                (user_id,kind,))
            con.commit()
            recodes = cursor.fetchall()

        w_list = [wishList.find(recode[0]) for recode in recodes]
        return w_list

    @staticmethod
    def search(user_id,word):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM table_wishList WHERE name LIKE '{}%' OR kind LIKE '{}%' AND user_id = {}".format(word,word,user_id)
            print(sql)
            cursor.execute(sql)
            con.commit()
            results = cursor.fetchall()

        records = []
        # print(results)
        for data in results:
            w = wishList()
            w.attr["id"] = data["id"]
            w.attr["user_id"] = data["user_id"]
            w.attr["name"] = data["name"]
            w.attr["quantity"] = data["quantity"]
            w.attr["kind"] = data["kind"]
            w.attr["last_updated"] = data["last_updated"]
            records.append(w)

        return records
