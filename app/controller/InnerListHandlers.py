import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.innerList import innerList
from controller.AuthenticationHandlers import SigninBaseHandler

class InnerCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # パラメータを取得
        _fridge_id = self.get_argument("fridge_id", None)

        f = fridge.build()
        self.render("inner_form.html",
                    user=_signedInUser,
                    fridge_id=_fridge_id,
                    mode="new",
                    fridge=f,
                    messages=[],
                    errors=[])


    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_fridge = self.get_argument("form-fridge", None)
        p_product_name = self.get_argument("form-product_name", None)
        p_lim = self.get_argument("form-lim", None)
        p_amount = self.get_argument("form-amount", None)
        p_whose = self.get_argument("form-whose", None)
        p_class = self.get_argument("form-class", None)


        # 現金出納帳データの組み立て
        cb = cashbook.build()
        cb.attr["user_id"] = int(_id)  # ユーザーIDはサインインユーザーより取得

        # パラメータエラーチェック
        errors = []
        if p_date is None:
            errors.append("日付は必須です。")
        else:
            # 文字列をdatetime.dateオブジェクトへをキャスト
            cb.attr["date"] = datetime.datetime.strptime(
                p_date, '%Y-%m-%d').date()
            # 年月計算
            cb.attr["ym"] = cb.attr["date"].year * 100 + cb.attr["date"].month

        if p_summary is None:
            errors.append("摘要は必須です。")
        cb.attr["summary"] = p_summary
        cb.attr["detail"] = p_detail

        if p_income is None and p_expenses is None:
            errors.append("収入/支出のどちらかは入力してください。")
        if p_income is None:
            p_income = 0
        if p_expenses is None:
            p_expenses = 0
        cb.attr["income"] = Decimal(p_income)
        cb.attr["expenses"] = Decimal(p_expenses)
        # 金額計算(収入 - 支出)
        cb.attr["amount"] = cb.attr["income"] - cb.attr["expenses"]

        if len(errors) > 0:  # エラーは新規登録画面に渡す
            self.render("cashbook_form.html",
                        user=_signedInUser,
                        mode="new",
                        cashbook=cb,
                        messages=[],
                        errors=[])
            return

        # 登録
        print(vars(cb))
        cb_id = cb.save()
        if cb_id == False:
            self.render("cashbook_form.html",
                        user=_signedInUser,
                        mode="new",
                        cashbook=cb,
                        messages=[],
                        errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/cashbooks?message=%s" %
                          tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % cb_id))

class InnerListHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # 他の画面からのメッセージを取得
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)

        # パラメータを取得
        _fridge_id = self.get_argument("fridge_id", None)
        # ユーザーごとの現金出納帳データを取得
        results = innerList.select_by_fridge_id(_fridge_id)
        self.render("innerList.html",
                    user=_signedInUser,
                    cashbooks=results,
                    messages=messages,
                    errors=[])
