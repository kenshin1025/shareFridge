
import tornado.web
import MySQLdb
import datetime
import json
from decimal import Decimal
from model.project import project
from model.user import user
from db import DBConnector
from controller.AuthenticationHandlers import SigninBaseHandler


class SortHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT
                    *
                FROM
                    table_cashbook
                ORDER BY
                    id;
            """)
            results = cursor.fetchall()
        if (len(results) == 0):
            print(None)
            return None

        cash_attrs = [
            "id",
            "user_id",
            "ym",
            # "data",
            # "summary",
            # "detail",
            # "income",
            # "expenses",
            # "amount",
            # "last_updated"
        ]
        response = {}

        self.write("[".encode())
        for data in results:
            for attr in cash_attrs:
                if(attr == "data"):
                    response["%s" % attr] = str(data["%s" % attr])
                else:
                    response["%s" % attr] = data["%s" % attr]
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(json.dumps(response))
            if(results[-1] != data):
                self.write(','.encode())
        self.write("]".encode())

        # response["id"] = []
        # response["user_id"] = []
        # response["ym"] = []
        # response["date"] = []
        # response["summary"] = []
        # response["detail"] = []
        # response["income"] = []
        # response["expenses"] = []
        # response["amount"] = []
        # response["last_updated"] = []
        # for data in results:
            # response["user_id"].append(str(data["user_id"]))
            # response["ym"].append(str(data["ym"]))
            # response["date"].append(data["date"])
            # response["summary"].append(str(data["summary"]))
            # response["detail"].append(str(data["detail"]))
            # response["income"].append(str(data["income"]))
            # response["expenses"].append(str(data["expenses"]))
            # response["amount"].append(str(data["amount"]))
            # response["last_updated"].append(str(data["last_updated"]))


class SortRenderHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        self.render("cash_sort.html")
