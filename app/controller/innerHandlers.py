import tornado.web
import datetime
from decimal import Decimal
from model.user import user
from model.innerList import innerList
from controller.AuthenticationHandlers import SigninBaseHandler

class innerListsHandler(SigninBaseHandler):
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
        if _message is not None: messages.append(_message)

         # ユーザーごとの現金出納帳データを取得
        results = innerList.select_by_user_id(_signedInUser.attr["id"])
        self.render("innerLists.html", user=_signedInUser, innerLists=results, messages=messages, errors=[])

        """# 概要を取得
        _product_name = self.get_argument("product_name", None)
        _whose = self.get_argument("whose", None)
        _kind = self.get_argument("kind", None)

        # ユーザーごとの現金出納帳データを取得
        if _product_name is not None:
            results = innerList.product_name(_id,_product_name)

        if _whose is not None:
            results = innerList.whose(_id,_whose)

        if _kind is not None:
            results = innerList._kind(_id,_kind)
        else:
            results = innerList.select_by_user_id(_signedInUser.attr["id"])
        self.render("search.html",
            user=_signedInUser,
            search=results,
            messages=messages,
            name=_name,
            kind=_kind,
            errors=[])"""

class WishShowHandler(SigninBaseHandler):
    def get(self, id):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        il = innerList.find(id)
        if il is None: raise tornado.web.HTTPError(404) # データが見つからない場合は404エラーを返す
        if il.attr["user_id"] != _signedInUser.attr["id"]: raise tornado.web.HTTPError(404) # ユーザーIDが異なる場合も404エラーを返す

        self.render("cashbook_form.html", user=_signedInUser, mode="show", innerList=il, messages=[], errors=[])

class WishCreateHandler(SigninBaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        il = innerList.build()
        self.render("innerList_form.html", user=_signedInUser, mode="new", innerList=il, messages=[], errors=[])

    def post(self):
        if not self.current_user:
            self.redirect("/signin")
            return
        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _signedInUser = user.find(int(_id))

        # POSTされたパラメータを取得
        p_product_name = self.get_argument("form-product_name", None)
        p_lim = self.get_argument("form-lim", None)
        p_amount = self.get_argument("form-amount",None)
        p_whose = self.get_argument("form-whose", None)
        p_kind = self.get_argument("form-kind", None)


        # 現金出納帳データの組み立て
        il = innerList.build()
        il.attr["user_id"] = int(_id) # ユーザーIDはサインインユーザーより取得

        errors = []
        if p_product_name is None: errors.append("品名は必須です。")
        il.attr["product_name"] = p_product_name

        if p_lim is None: errors.append("個数は必須です。")
        il.attr["lim"] = p_lim

        if p_whose is None: errors.append("誰のものかは必須です。")
        il.attr["whose"] = p_whose

        if p_kind is None: errors.append("分類は必須です。")
        il.attr["kind"] = p_kind

        il.attr["amount"] = int(p_amount)
        #w.attr["last_updated"] = p_last_updated

        if len(errors) > 0: # エラーは新規登録画面に渡す
            self.render("innerList_form.html", user=_signedInUser, mode="new", innerList=il, messages=[], errors=[])
            return

        # 登録
        # print(vars(w))
        w_id = w.save()
        if w_id == False:
            self.render("innerList_form.html", user=_signedInUser, mode="new", innerList=w, messages=[], errors=["登録時に致命的なエラーが発生しました。"])
        else:
            # 登録画面へリダイレクト(登録完了の旨を添えて)
            self.redirect("/innerLists?message=%s" % tornado.escape.url_escape("新規登録完了しました。(ID:%s)" % w_id))
