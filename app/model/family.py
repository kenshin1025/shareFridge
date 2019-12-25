import MySQLdb
import datetime

from db import DBConnector
from model.project import project

class family:
    """ユーザーモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["id"] = None              # id int notNull
        self.attr["name"] = None            # name str notNull
        self.attr["pass"] = None        # password str notNull

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_family;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_family` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `name` varchar(255) DEFAULT NULL,
                    `password` varchar(255) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `OUTER_KEY` (`name`),
                    KEY `KEY_INDEX` (`name`)
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
                FROM   table_family
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        f = family()
        f.attr["id"] = data["id"]
        f.attr["name"] = data["name"]
        f.attr["password"] = data["password"]
        return f

    @staticmethod
    def build():
        f = family()
        return f

    def is_valid(self):
        return all([
          self.attr["id"] is None or type(self.attr["id"]) is int,
          self.attr["name"] is not None and type(self.attr["name"]) is str,
          self.attr["password"] is not None and type(self.attr["password"]) is str,
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
                INSERT INTO table_family
                    (name, password)
                VALUES
                    (%s, %s); """,
                (self.attr["name"],self.attr["password"],))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_family
                SET name = %s,
                    password = %s
                WHERE id = %s; """,
                (self.attr["name"],
                self.attr["password"],
                self.attr["id"]))

            con.commit()

        return self.attr["id"]