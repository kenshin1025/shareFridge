import MySQLdb
import datetime

from db import DBConnector
from model.project import project

class fridge:
    
    def __init__(self):
        self.attr = {}
        self.attr["id"] = None
        self.attr["famiry_id"] = None
    
    @staticmethod
    def migrate():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' % project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_fridge;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_fridge` (
                    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `famiry_id` int(11) unsigned NOT NULL,
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
                FROM   table_fridge
                WHERE  id = %s;
            """, (id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        f = fridge()
        f.attr["id"] = data["id"]
        f.attr["famiry_id"] = data["famiry_id"]
        return f

    @staticmethod
    def build():
        f=fridge()
        return f

    def is_valid(self):
        return all([
            self.attr["id"] is None or type(self.attr["id"]) is int,
            self.attr["famiry_id"] is not None and type(self.attr["famiry_id"]) is int,
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
            
            cursor.execute("""
                INSERT INTO table_fridge
                    (famiry_id)
                VALUES
                    (%s);""",
                (self.attr["famiry_id"],))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["id"] = results[0]

            con.commit()

        return self.attr["id"]

    def _db_save_update(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                UPDATE table_fridge
                SET famiry_id = %s
                WHERE id = %s; """,
                (
                self.attr["famiry_id"],
                self.attr["id"]
                ))

            con.commit()

        return self.attr["id"]
