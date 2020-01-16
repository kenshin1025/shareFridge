#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import sys
from model.cashbook import cashbook
from model.user import user
from controller.AuthenticationHandlers import SigninBaseHandler, SigninHandler, SignupHandler, SignoutHandler
from controller.CashBookHandlers import CashbookCreateHandler, CashbooksHandler, CashbookShowHandler
from controller.WebAPIHandlers import IncomeRankHandler, ExpensesRankHandler, MonthlyReportHandler
from controller.InnerListHandlers import InnerListHandler, InnerCreateHandler


class MainHandler(SigninBaseHandler):  # 継承元がSigninBaseHandlerになっているので注意
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))
        # ダッシュボードを表示
        self.render("dashboard.html", user=_signedInUser)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/signin", SigninHandler),
    (r"/signup", SignupHandler),
    (r"/signout", SignoutHandler),
    (r"/inner", InnerListHandler),
    (r"/cashbook/new", CashbookCreateHandler),  # 現金出納帳 新規作成
    (r"/cashbooks", CashbooksHandler),
    (r"/cashbook/show/([0-9]+)", CashbookShowHandler),
    (r"/api/incomerank", IncomeRankHandler),    # 摘要別収入ランキング
    (r"/api/expensesrank", ExpensesRankHandler),  # 摘要別支出ランキング
    (r"/api/monthlyreport/([0-9]+)", MonthlyReportHandler),  # 月別日別レポート
],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(),  "static"),
    # cookieの暗号化キー(システムごとにランダムな文字列を設定する)
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",
)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "migrate":
            cashbook.migrate()
            user.migrate()
        if args[1] == "db_cleaner":
            cashbook.db_cleaner()
            user.db_cleaner()
        if args[1] == "help":
            print("usage: python server.py migrate # prepare DB")
            print("usage: python server.py db_cleaner # remove DB")
            print("usage: python server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
